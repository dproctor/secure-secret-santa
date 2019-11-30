# Secure Secret Santa

## Installation
```
pip install -r requirements.txt
```

## Usage

This script can be used in three different modes:
1. generate a keypair

```
python assign_pairings.py  --create_key
```

will create two files: private.pem, public.pem. private.pem is your private
key. Keep this safe and don't share it with anyone! Email public.pem to
Devon.

2. assign pairings

```
python assign_pairiings.py
```

actually creates the assignment by randomly sampling all permutations, and
rejecting candidate pairings that don't satisfy the conditions of a valid
pairing. Right now, this enforces that no one gives to themselves, and that
no one gives to their partner. We might consider adding that no two people
give to each other, or other such conditions.

3. reveal assignments

```
python assign_pairiings.py  \
  --assignment assignments/{YOUR_NAME} \
  --private_key {YOUR_PRIVATE_KEY}
```

reveals your assignment. Make sure no one is looking over your
shoulder when you run this command :P
