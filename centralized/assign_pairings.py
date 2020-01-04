#! /usr/bin/python
"""
Implements secure secret santa assignments via rejection sampling.

This script can be used in three different modes:
1. generate a keypair

    python assign_pairings.py  --create_key

    will create two files: private.pem, public.pem. private.pem is your private
    key. Keep this safe and don't share it with anyone! email public.pem to
    Devon.

2. assign pairings

    python assign_pairings.py

    actually creates the assignment by randomly sampling all permutations, and
    rejecting candidate pairings that don't satisfy the conditions of a valid
    pairing. Right now, this enforces that no one gives to themselves, and that
    no one gives to their partner. We might consider adding that no two people
    give to each other, or other such conditions.

3. reveal assignments

    python assign_pairings.py  \
        --assignment assignments/{YOUR_NAME} \
        --private_key {YOUR_PRIVATE_KEY}

    this reveals your assignment. Make sure no one is looking over your
    shoulder when you run this command :P
"""

from __future__ import print_function

import argparse
import random
import sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

PARTICIPANTS = {
    b"Chris": {
        "public_key": "keys/chris.pub",
        "assignment": "assignments/chris"
    },
    b"Zuz": {
        "public_key": "keys/zuz.pub",
        "assignment": "assignments/zuz"
    },
    b"Haley": {
        "public_key": "keys/haley.pub",
        "assignment": "assignments/haley"
    },
    b"Amelia": {
        "public_key": "keys/amelia.pub",
        "assignment": "assignments/amelia"
    },
    b"Devon": {
        "public_key": "keys/devon.pub",
        "assignment": "assignments/devon"
    },
    b"Caitlin": {
        "public_key": "keys/caitlin.pub",
        "assignment": "assignments/caitlin"
    },
    b"Doug": {
        "public_key": "keys/doug.pub",
        "assignment": "assignments/doug"
    },
    b"Katie": {
        "public_key": "keys/katie.pub",
        "assignment": "assignments/katie"
    },
}

COUPLES = {
    b"Chris": 1,
    b"Zuz": 1,
    b"Haley": 2,
    b"Amelia": 2,
    b"Devon": 3,
    b"Caitlin": 3,
    b"Doug": 4,
    b"Katie": 4
}

MAX_ITERATIONS = 1e10


def _is_valid_pairing(pairing):
    for giver, receiver in pairing.items():
        if giver == receiver:
            return False
        if COUPLES[giver] == COUPLES[receiver]:
            return False
    return True


def _generate_key():
    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=2048,
                                           backend=default_backend())
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    with open('private.pem', 'wb') as out_file:
        out_file.write(pem)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open('public.pem', 'wb') as out_file:
        out_file.write(pem)


def _reveal_assignment(assignment, private_key):
    with open(private_key, "rb") as serialized_key:
        private_key = serialization.load_pem_private_key(
            serialized_key.read(), password=None, backend=default_backend())
        with open(assignment, "rb") as encrypted:
            receiver = private_key.decrypt(
                encrypted.read(),
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                             algorithm=hashes.SHA256(),
                             label=None))
        print("You're buying a gift for {}".format(receiver))
    pass


# pylint: disable=missing-docstring
def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--create_key',
        help="Creates public and private keys at public.pem and private.pem",
        action="store_true")

    parser.add_argument(
        '--assignment',
        help="Reveals the assignment. You must also provide --private_key.",
        type=str)

    parser.add_argument(
        '--private_key',
        help=
        "Private key for decrypting your assignment. Must also provide --assingment",
        type=str)

    parser.add_argument('--reveal',
                        help="Reveals the assignment, for debugging.",
                        action="store_true")

    args = parser.parse_args(arguments)

    if args.create_key:
        _generate_key()
        return

    if args.assignment:
        assert args.private_key, "To reveal your assignment, you must also provide a --private_key."
        _reveal_assignment(args.assignment, args.private_key)
        return

    i = 0
    while i < MAX_ITERATIONS:
        permutation = list(range(len(PARTICIPANTS)))
        random.shuffle(permutation)
        candidate_pairing = {
            list(PARTICIPANTS.keys())[i]:
            list(PARTICIPANTS.keys())[permutation[i]]
            for i in range(len(permutation))
        }
        if not _is_valid_pairing(candidate_pairing):
            i += 1
            continue
        print("Found pairing after {} attempts\n".format(i))
        for giver, receiver in candidate_pairing.items():
            with open(PARTICIPANTS[giver]["public_key"],
                      "rb") as serialized_key:
                public_key = serialization.load_pem_public_key(
                    serialized_key.read(), backend=default_backend())
                encrypted = public_key.encrypt(
                    receiver,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                 algorithm=hashes.SHA256(),
                                 label=None))

                with open(PARTICIPANTS[giver]["assignment"],
                          "wb") as assignment:
                    assignment.write(encrypted)
                if args.reveal:
                    print("{:<7} gives to {:<7}".format(
                        giver.decode(), receiver.decode()))
        break


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
