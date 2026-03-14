Quick Resolution Found!

If you are getting `name 'JavaClass' is not defined`, this means one of two things.

1. You are trying to use a pyjinn script with a .py extension.
> Pyjinn files need to have a .pyj extension to work properly. The pyjinn file you are trying to run is expecting to be ran under the pyjinn executor. If you are importing an existing .py file and get this result, this means that your `main` file needs to have a .py extension.

2. You forgot to import JavaClass
> Pyjinn automatically comes with the `JavaClass` feature defined. If you are using it in a python script, you must use:

```py
from java import JavaClass # MS v5.0+

from lib_java import JavaClass #MS v4.0 (needs download from MS site)
```

[lib_java download](<https://minescript.net/sdm_downloads/lib_java-v2>)