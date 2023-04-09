# Multiple-Inclusion Optimization Test

Below are a list of different methods (some very far fetched) to guard a C/C++
header files and whether the compilers will avoid opening and preprocessing
those files if they are `#include`d after the first time.  This is called
the [multiple-inclusion optimization](https://gcc.gnu.org/onlinedocs/cppinternals/Guard-Macros.html).

| Name                                                                | clang | gcc | msvc |
| ------------------------------------------------------------------- | ----- | --- | ---- |
| [`include-guard`](guards/include-guard)                             | yes   | yes | yes  |
| [`pragma-twice`](guards/pragma-twice)                               | yes   | yes | yes  |
| [`pragma-once`](guards/pragma-once)                                 | yes   | yes | yes  |
| [`conditional-define`](guards/conditional-define)                   | yes   | yes | yes  |
| [`transitive-self-inclusion`](guards/transitive-self-inclusion)     | yes   | yes | yes  |
| [`pragma-anywhere`](guards/pragma-anywhere)                         | yes   | yes | yes  |
| [`self-inclusion`](guards/self-inclusion)                           | yes   | yes | yes  |
| [`between-guard`](guards/between-guard)                             | yes   | yes | yes  |
| [`include-guard-twice`](guards/include-guard-twice)                 | yes   | yes | yes  |
| [**`if-not-defined-recursive`**](guards/if-not-defined-recursive)   | yes   | yes |**no**|
| [**`if-not-defined`**](guards/if-not-defined)                       | yes   | yes |**no**|
| [**`ms-pragma-once`**](guards/ms-pragma-once)                       | yes   | yes |**no**|
| [**`already-guarded`**](guards/already-guarded)                     | **no**| yes | yes  |
| [**`null-directive-outside`**](guards/null-directive-outside)       | **no**| yes | yes  |
| [`if-guard-not-expr`](guards/if-guard-not-expr)                     | no    | no  |  no  |
| [`unguarded`](guards/unguarded)                                     | no    | no  |  no  |
| [`if-guard-not-1`](guards/if-guard-not-1)                           | no    | no  |  no  |
| [`decl-outside`](guards/decl-outside)                               | no    | no  |  no  |
| [`if-guard-expr`](guards/if-guard-expr)                             | no    | no  |  no  |
| [`pragma-def-once`](guards/pragma-def-once)                         | no    | no  |  no  |
| [`if-guard-1`](guards/if-guard-1)                                   | no    | no  |  no  |
| [`split-include-guard`](guards/split-include-guard)                 | no    | no  |  no  |
| [`if-0`](guards/if-0)                                               | no    | no  |  no  |
| [`reverse-guard`](guards/reverse-guard)                             | no    | no  |  no  |
| [`if-guard-42`](guards/if-guard-42)                                 | no    | no  |  no  |
    

## Raw Results

### clang

```$ clang --version
clang version 10.0.0-4ubuntu1
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin

$ ./run.py clang
Guarded (12)
  - include-guard (401ms)
  - pragma-twice (411ms)
  - pragma-once (426ms)
  - conditional-define (444ms)
  - transitive-self-inclusion (449ms)
  - pragma-anywhere (454ms)
  - if-not-defined-recursive (485ms)
  - if-not-defined (501ms)
  - self-inclusion (513ms)
  - ms-pragma-once (520ms)
  - between-guard (539ms)
  - include-guard-twice (615ms)
Unguarded (13)
  - already-guarded (1500ms)
  - if-guard-not-expr (1554ms)
  - unguarded (1555ms)
  - if-guard-not-1 (1582ms)
  - decl-outside (1594ms)
  - if-guard-expr (1596ms)
  - pragma-def-once (1600ms)
  - split-include-guard (1603ms)
  - null-directive-outside (1611ms)
  - if-guard-1 (1613ms)
  - if-0 (1618ms)
  - reverse-guard (1621ms)
  - if-guard-42 (1694ms)
```

### gcc 9.4.0

```$ gcc --version
gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
Copyright (C) 2019 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ ./run.py gcc
Guarded (14)
  - pragma-twice (13ms)
  - pragma-anywhere (14ms)
  - conditional-define (14ms)
  - ms-pragma-once (14ms)
  - transitive-self-inclusion (14ms)
  - pragma-once (16ms)
  - include-guard (16ms)
  - if-not-defined-recursive (16ms)
  - if-not-defined (17ms)
  - already-guarded (17ms)
  - between-guard (18ms)
  - include-guard-twice (18ms)
  - self-inclusion (19ms)
  - null-directive-outside (19ms)
Unguarded (11)
  - pragma-def-once (1471ms)
  - if-guard-1 (1476ms)
  - if-0 (1483ms)
  - if-guard-not-1 (1484ms)
  - reverse-guard (1492ms)
  - decl-outside (1501ms)
  - unguarded (1506ms)
  - split-include-guard (1509ms)
  - if-guard-expr (1534ms)
  - if-guard-not-expr (1535ms)
  - if-guard-42 (1543ms)
```

### Microsoft Visual Studio 2022

```cl
Microsoft (R) C/C++ Optimizing Compiler Version 19.31.31105 for x86
Copyright (C) Microsoft Corporation.  All rights reserved.
```

```run.py msvc
Guarded (11)
  - include-guard (120ms)
  - pragma-twice (121ms)
  - conditional-define (127ms)
  - pragma-anywhere (129ms)
  - between-guard (132ms)
  - pragma-once (132ms)
  - self-inclusion (136ms)
  - null-directive-outside (138ms)
  - include-guard-twice (138ms)
  - transitive-self-inclusion (147ms)
  - already-guarded (260ms)
Unguarded (14)
  - unguarded (27366ms)
  - if-guard-1 (28629ms)
  - ms-pragma-once (28673ms)
  - decl-outside (28719ms)
  - if-guard-not-expr (29043ms)
  - if-0 (29442ms)
  - if-not-defined-recursive (29474ms)
  - if-not-defined (29551ms)
  - split-include-guard (29988ms)
  - reverse-guard (30088ms)
  - pragma-def-once (30148ms)
  - if-guard-not-1 (30508ms)
  - if-guard-expr (32925ms)
  - if-guard-42 (33698ms)
```
