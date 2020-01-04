Participants A = {a_0, ..., a_n}

Exclusion sets X_i = {b_0, ..., b__m}

A, X_i all public.

All participants a_i go to www.$DOMAIN_NAME/room/$ROOM_NAME.

# Server endpoints:

1. /room/$ROOM_NAME static, serves resources for js app.
2. /channel configures webrtc channel

# Algorithm

1. Shared SALT generated together, concatenation of individual salts.
2. Each a_i makes private and public keys {Pu_i, Pr_i} based on SALT and
   publishes Pu_i.
3.
```
def attempt_assignment() -> bool:
"""
Attempts to create an assignment by proceeding through participants in turn.

Each participant selects a random recipient, and checking with each previous
participant whether that recipient has already been claimed. If there is a
conflict, returns false.

The group runs this algorithm until success.
"""
  for a_i in A:
    set_seed(Pr_i)
    r_i = select_random_element(A - X_i)
    for j : j < i:
      if check_conflict(a_j):
        return False
  return True


def check_conflict(person_to_check_with) -> bool :
"""
Called by a_i to check whether their recipient conflicts with a_j's recipient.

This is done in a way such that if a_i and a_j do not conflict, a_i and a_j
learn nothing about the other's recipient.

a_i, a_j pick one way functions f_i, f_j, respectively, such that

f_i(f_j(r_j)) == f_j(f_i(r_i))     <=>     r_i == r_j

a_i                                 a_j
 |      --------f_i(r_i)------>      |
 |      <-------f_j(r_j)-------      |
 |                                   |
 |      ----f_i(f_j(r_j))----->      |
 |      <---f_j(f_i(r_i))------      |

Then, both a_i, a_j can check whether r_i == r_j
"""
```
