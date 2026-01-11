import pyshark
import sys

FILETYPES = ['pcapng', 'pcap', 'cap']
OUTPUT_FORMATS = ['hashcat', 'john']
SUPPORTED_ETYPES = ['18', '23']

def get_hashes(file, output_format):
    try:
        capture = pyshark.FileCapture(
            file,
            display_filter='kerberos.msg_type == 10' # AS-REQ packets
        )
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

    hashes = [].

    for packet in capture:
        etype = None
        cipher = None
        realm = None
        user = None

        hash_string = None

        try:
            etype = packet.kerberos.get("etype")

            if etype not in SUPPORTED_ETYPES:
                continue

            cipher = packet.kerberos.get("cipher").replace(':', '')

            if etype == '23':
                cipher = cipher[32:] + cipher[:32] # Move HMAC to the end

            realm = packet.kerberos.get("realm")
            user = packet.kerberos.get("CNameString")

        except AttributeError:
            continue

        match etype:
            case '18':
                # $krb5pa$etype$user$realm$cipher
                if output_format == 'john': # John needs salt specified
                    hash_string = f"$krb5pa${etype}${user}${realm}${realm}{user}${cipher}"
                else: # Hashcat uses the default salt
                    hash_string = f"$krb5pa${etype}${user}${realm}${cipher}"

            case '23':
                # $krb5pa$etype$user$realm$salt$cipher+HMAC(128bits=32chars)

                # The default salt string, if none is provided via
                # pre-authentication data, is the concatenation of
                # the principal's realm and name components, in order,
                # with no separators.
                # https://datatracker.ietf.org/doc/html/rfc4120#section-4

                # Therefore we use the default salt here
                hash_string = f"$krb5pa${etype}${user}${realm}${realm}{user}${cipher}"

        if hash_string not in hashes:
            hashes.append(hash_string)

    return hashes

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) != 2:
        print("Usage: python shark2authdog.py <pcap_file> <output_format: 'hashcat' or 'john'>")
        sys.exit(1)

    if args[0].split('.')[-1] not in FILETYPES:
        print("Invalid file format")
        sys.exit(1)

    if args[1].lower() not in OUTPUT_FORMATS:
        print("Invalid output format. Must be 'hashcat' or 'john'")
        sys.exit(1)

    for h in get_hashes(args[0], args[1].lower()):
        print(h)
