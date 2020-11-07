# ECS240 Programming Assignment 2

## Task Planning
1. Input and output 
    - Andersen algorithm [implemented]
    - Chakaravarthy's algorithm
        - input [implemented]
        - output [todo]
2. Rewrite the statements and extend the reference and dereference[implemented][todo test][todo quicker algorithm]
3. Andersen's algorithm [implemented][todo test][todo test pairs operations]
    - address_of(statement)
    - alias_of(pairs, statement)
    - assign_of(pairs, statement)
    - deref_of(pairs, statement)
4. Chakaravarthy's algorithm (to discuss data structure)
    - Direct assignments [implemented][todo test]
    - Copying statements [implemented][todo test]
    - Edge computation
    - Forbidden Pair computation (?)
    - main algorithm (Figure 4.) [implemented][todo test]

5. Data structures (dict and set)

    5.1 `class LayeredGraph()` 
    - `kGenerationSuccessors()` [implemented][tested]
    - `checkConnected()` [implemented][tested]
    - `dualNodeGraph()` [implemented][todo test][risk]
    - `checkPathVertexDisjoint()` [implemented][todo test][risk]

    5.2 `class ForbiddenPair()`
    - `cumulate()` [implemented][todo test]
    
    5.3 `class ConcurrentCopyPropagation()`

    - `solve1ccp()` [implemented][tested]
    - `solve2ccp()` [implemented][tested]

6. Test (find some examples in lecture slides)
