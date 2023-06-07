# Multiple-Inclusion Optimization Test

Below are a list of different methods (some very far fetched) to guard a C/C++
header files and whether the compilers will avoid opening and preprocessing
those files if they are `#include`d after the first time.  This is called
the [multiple-inclusion optimization](https://gcc.gnu.org/onlinedocs/cppinternals/Guard-Macros.html).

## Compiler Agreement

Clang, gcc, and Visual Studio agree on the following guards and whether they
are eligible for the optimization.

| Name                                                                | Clang | gcc | msvc |
| ------------------------------------------------------------------- | ----- | --- | ---- |
| [`pragma-once`](guards/pragma-once)                                 | yes   | yes | yes  |
| [`pragma-twice`](guards/pragma-twice)                               | yes   | yes | yes  |
| [`pragma-anywhere`](guards/pragma-anywhere)                         | yes   | yes | yes  |
| [`_pragma-once`](guards/_pragma-once)                               | yes   | yes | yes  |
| [`_pragma-def-once`](guards/_pragma-def-once)                       | yes   | yes | yes  |
| [`include-guard`](guards/include-guard)                             | yes   | yes | yes  |
| [`include-guard-twice`](guards/include-guard-twice)                 | yes   | yes | yes  |
| [`conditional-define`](guards/conditional-define)                   | yes   | yes | yes  |
| [`between-guard`](guards/between-guard)                             | yes   | yes | yes  |
| [`transitive-self-inclusion`](guards/transitive-self-inclusion)     | yes   | yes | yes  |
| [`self-inclusion`](guards/self-inclusion)                           | yes   | yes | yes  |
| [`if-0`](guards/if-0)                                               | no    | no  | no   |
| [`if-guard-1`](guards/if-guard-1)                                   | no    | no  | no   |
| [`if-guard-not-1`](guards/if-guard-not-1)                           | no    | no  | no   |
| [`if-guard-42`](guards/if-guard-42)                                 | no    | no  | no   |
| [`if-guard-expr`](guards/if-guard-expr)                             | no    | no  | no   |
| [`if-guard-not-expr`](guards/if-guard-not-expr)                     | no    | no  | no   |
| [`split-include-guard`](guards/split-include-guard)                 | no    | no  | no   |
| [`decl-outside`](guards/decl-outside)                               | no    | no  | no   |
| [`reverse-guard`](guards/reverse-guard)                             | no    | no  | no   |
| [`unguarded`](guards/unguarded)                                     | no    | no  | no   |

## Compiler Disagreement


Clang, gcc, and Visual Studio **disagree** on the following guards and whether
they are eligible for the optimization.

| Name                                                                | Clang    | gcc    | msvc   |
| ------------------------------------------------------------------- | -------- | ------ | ------ |
| [**`__pragma-once`**](guards/__pragma-once)                         | **no**   | **no** |   yes  |
| [**`if-not-defined`**](guards/if-not-defined)                       |   yes    |   yes  | **no** |
| [**`if-not-defined-recursive`**](guards/if-not-defined-recursive)   |   yes    |   yes  | **no** |
| [**`already-guarded`**](guards/already-guarded)                     | **no**   |   yes  |   yes  |
| [**`null-directive-outside`**](guards/null-directive-outside)       | **no**\* |   yes  |   yes  |

\* fixed in Clang 17 ([D147928](https://reviews.llvm.org/D147928)).

Note that there is an additional,
[outstanding performance issue in GCC](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58770)
when using `#pragma once` that is not shown in these benchmarks.

## Raw Results

### clang

```$ clang --version
clang version 10.0.0-4ubuntu1
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin

$ ./run.py clang
Guarded (13)
  - if-not-defined (189ms)
  - pragma-anywhere (191ms)
  - include-guard (200ms)
  - pragma-once (210ms)
  - include-guard-twice (213ms)
  - _pragma-once (222ms)
  - transitive-self-inclusion (224ms)
  - _pragma-def-once (230ms)
  - conditional-define (236ms)
  - self-inclusion (236ms)
  - pragma-twice (242ms)
  - if-not-defined-recursive (249ms)
  - between-guard (268ms)
Unguarded (13)
  - already-guarded (670ms)
  - if-0 (678ms)
  - if-guard-not-expr (681ms)
  - if-guard-not-1 (688ms)
  - split-include-guard (695ms)
  - if-guard-42 (700ms)
  - null-directive-outside (709ms)
  - if-guard-1 (717ms)
  - if-guard-expr (740ms)
  - reverse-guard (752ms)
  - decl-outside (917ms)
  - unguarded (972ms)
  - __pragma-once (1042ms)
```

### gcc 9.4.0

```$ gcc --version
gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
Copyright (C) 2019 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ ./run.py gcc
Guarded (15)
  - _pragma-once (346ms)
  - already-guarded (347ms)
  - if-not-defined-recursive (349ms)
  - conditional-define (355ms)
  - if-not-defined (357ms)
  - _pragma-def-once (359ms)
  - pragma-once (376ms)
  - pragma-twice (432ms)
  - include-guard-twice (432ms)
  - include-guard (435ms)
  - self-inclusion (441ms)
  - null-directive-outside (447ms)
  - pragma-anywhere (447ms)
  - transitive-self-inclusion (453ms)
  - between-guard (470ms)
Unguarded (11)
  - if-guard-not-expr (990ms)
  - __pragma-once (1017ms)
  - if-guard-expr (1061ms)
  - unguarded (1070ms)
  - decl-outside (1091ms)
  - if-0 (1092ms)
  - if-guard-42 (1100ms)
  - if-guard-not-1 (1109ms)
  - if-guard-1 (1110ms)
  - split-include-guard (1124ms)
  - reverse-guard (1127ms)
```

### Microsoft Visual Studio 2022

```$ cl
Microsoft (R) C/C++ Optimizing Compiler Version 19.31.31105 for x86
Copyright (C) Microsoft Corporation.  All rights reserved.

$ .\run.py msvc
Guarded (14)
  - null-directive-outside (114ms)
  - _pragma-once (114ms)
  - pragma-twice (115ms)
  - include-guard-twice (116ms)
  - _pragma-def-once (119ms)
  - pragma-once (120ms)
  - pragma-anywhere (123ms)
  - include-guard (128ms)
  - transitive-self-inclusion (129ms)
  - __pragma-once (131ms)
  - self-inclusion (134ms)
  - conditional-define (155ms)
  - between-guard (157ms)
  - already-guarded (277ms)
Unguarded (12)
  - if-guard-42 (2273ms)
  - if-not-defined (2286ms)
  - if-guard-expr (2286ms)
  - if-not-defined-recursive (2295ms)
  - if-guard-not-1 (2297ms)
  - reverse-guard (2300ms)
  - unguarded (2304ms)
  - if-0 (2310ms)
  - split-include-guard (2326ms)
  - if-guard-not-expr (2332ms)
  - if-guard-1 (2343ms)
  - decl-outside (2484ms)
```
