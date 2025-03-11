# 🦈shark2authdog🌭

A python script to parse **Kerberos Pre-Authentication** (PA) **hashes** (krb5pa), **from Wireshark** capture files containing KRB5 **AS-REQ** packets. These can be given to either **hashcat** or **john the ripper** to crack the user's password.

Supports etype 18 (aes256-cts-hmac-sha1-96) & 23 (rc4-hmac), assuming *default salt strings*.

>The *default salt string*, if none is provided via pre-authentication data, is the concatenation of the principal's realm and name components, in order, with no separators.
[RFC4120 - Section 4](https://datatracker.ietf.org/doc/html/rfc4120#section-4)↗
## In action:

[Using a sample capture file](https://wiki.wireshark.org/SampleCaptures#kerberos-and-keytab-file-for-decryption)↗
```bash
[arianne@kitaria shark2authdog]$ python shark2authdog.py krb-816.cap hashcat
$krb5pa$23$des$DENYDC$DENYDCdes$32d396a914a4d0a78e979ba75d4ff53c1db7294141760fee05e434c12ecf8d5b9aa5839e09a2244893aff5f384f79c37883f154a
$krb5pa$23$u5$DENYDC$DENYDCu5$daf324dccec73739f6e49ef8fde60a9f9dfff50551ff5a7e969c6e395f18b842fb17c3b503df3025ab5a9dfc3031e893c4002008
$krb5pa$23$u5$DENYDC$DENYDCu5$addbe67ccf9dd3c3da9e233612816c5720447ae202cfe7a84a719e1ef70b93bcef49786f71319a93d60531fcb443f7e96039f540

[arianne@kitaria shark2authdog]$ hashcat -m 7500 hash.hash ~/wordlists/passwords/rockyou.txt
[...]
$krb5pa$23$des$DENYDC$DENYDCdes$32d396a914a4d0a78e979ba75d4ff53c1db7294141760fee05e434c12ecf8d5b9aa5839e09a2244893aff5f384f79c37883f154a:123
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 7500 (Kerberos 5, etype 23, AS-REQ Pre-Auth)
Hash.Target......: $krb5pa$23$des$DENYDC$DENYDCdes$32d396a914a4d0a78e9...3f154a
Time.Started.....: Sun Mar  9 23:07:02 2025 (0 secs)
Time.Estimated...: Sun Mar  9 23:07:02 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/home/arianne/wordlists/passwords/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.1.........:  1344.6 kH/s (7.78ms) @ Accel:16 Loops:1 Thr:8 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 12288/14344384 (0.09%)
Rejected.........: 0/12288 (0.00%)
Restore.Point....: 0/14344384 (0.00%)
Restore.Sub.1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.1....: 123456 -> havana

[arianne@kitaria shark2authdog]$
```
## Usage

1. Install dependencies:
```bash
pip install pyshark
```
2. Launch:
```bash
python shark2authdog.py <file> <output_format: 'hashcat' or 'john'>
```
3. Crack the found hash(es) with hashcat or john:

### hashcat
#### etype 18
```bash
hashcat -m 19900 hash.txt wordlist.txt
```

```bash
hashcat --show -m 19900 hash.txt
```
#### etype 23
```bash
hashcat -m 7500 hash.txt wordlist.txt
```

```bash
hashcat --show -m 7500 hash.txt
```

### john the ripper
```bash
john --wordlist=wordlist.txt hash.txt
```
```bash
john --show hash.txt
```
