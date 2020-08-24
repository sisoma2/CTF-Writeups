# Google CTF 2020 - Android

> Reversing
>
> Can you find the correct key to unlock this app?

## Solution

As the tittle of the challenge says it looks like we are presented with an APK so we will unpack the file with `apktool`.

```console
apktool d reverse.apk
```

If we take a look at the project structure and files, It looks like it's a simple APK, no native library, no third party frameworks like Flutter or Xamarin...

```console
rwxrwxrwx  1  root  root     4 KiB  Mon Aug 24 20:40:13 2020    ./
rwxrwxrwx  1  root  root     4 KiB  Mon Aug 24 20:40:09 2020    ../
rwxrwxrwx  1  root  root   712 B    Mon Aug 24 20:40:12 2020    AndroidManifest.xml
rwxrwxrwx  1  root  root   420 B    Mon Aug 24 20:40:13 2020    apktool.yml
rwxrwxrwx  1  root  root     4 KiB  Mon Aug 24 20:40:13 2020    original/
rwxrwxrwx  1  root  root     4 KiB  Mon Aug 24 20:40:12 2020    res/
rwxrwxrwx  1  root  root     4 KiB  Mon Aug 24 20:40:13 2020    smali/
```

Next, if we try to use JADX in order to reverse engineer de JAVA code we can see below that it fails to decompile some methods and won't be possible.

```java
public void onClick(android.view.View r1) {
/*
// Can't load method instructions: Load method exception: Not class type: long in method: com.google.ctf.sandbox.ő.1.onClick(android.view.View):void, dex: classes.dex
                */
	throw new UnsupportedOperationException("Method not decompiled: com.google.ctf.sandbox.C0009.C00101.onClick(android.view.View):void");
}
```

As JADX failed, we will have to work with the Smali code. If we open the APK in Android Studio we can see that the main class `ő.smali` has three fields.

```
# instance fields
.field class:[J

.field ő:I

.field ő:[J
```

The field `class` is an array and is initialized in the constructor with the following content:

```
0x271986b
0xa64239c9L
0x271ded4b
0x1186143
0xc0fa229fL
0x690e10bf
0x28dca257
0x16c699d1
0x55a56ffd
0x7eb870a1
0xc5c9799fL
0x2f838e65
```

Those are the twelve hashes that the application will check against the flag.

Next, if we analyze the `onClick`function in the `ő$1.smali`file, first we can see a large string with the content `Apparently this is not the flag. What's going on?` created byte by byte which is a false flag.

```
new-array v2, v2, [Ljava/lang/Object;

const/16 v8, 0x41  ---> 'A'

.line 45
invoke-static {v8}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

move-result-object v8

aput-object v8, v2, v3

const/16 v8, 0x70  ---> 'p'

invoke-static {v8}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

move-result-object v9

aput-object v9, v2, v6

invoke-static {v8}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

move-result-object v8

aput-object v8, v2, v5

const/16 v8, 0x61  ---> 'a'

invoke-static {v8}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

move-result-object v9

aput-object v9, v2, v4

const/16 v9, 0x72  ---> 'r'
```

Next, we can see that the routine checks the length of the input text. If the length is not 48 it prints the bad boy message.

```
.local v3, "flagString":Ljava/lang/String;
invoke-virtual {v3}, Ljava/lang/String;->length()I

move-result v5

const/16 v6, 0x30

if-eq v5, v6, :cond_21f

.line 62
iget-object v4, v1, Lcom/google/ctf/sandbox/ő$1;->val$textView:Landroid/widget/TextView;

const-string v5, "\u274c" ---> Bad boy ❌

invoke-virtual {v4, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
```

If we continue analyzing the function, we can see how it iterates the user input by four chars and calls the function `ő(JJ)`.

```
invoke-static {v8, v9, v4, v5}, Lcom/google/ctf/sandbox/R;->ő(JJ)[J
```

Analyzing the function `ő(JJ)` we see that this function is decompilable and it's the [Extended Euclidean Algorithm](https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/) [1].

```java
public static long[] m0(long a, long b) {
        if (a == 0) {
            return new long[]{0, 1};
        }
        long[] r = m0(b % a, a);
        return new long[]{r[1] - ((b / a) * r[0]), r[0]};
    }
```

Then it compares the hash calculated in the above function with the values hardcoded in the array. If they are not equal it prints the bad boy message.

```
.local v7, "inv":J
iget-object v9, v1, Lcom/google/ctf/sandbox/ő$1;->this$0:Lcom/google/ctf/sandbox/ő;

iget-object v9, v9, Lcom/google/ctf/sandbox/ő;->class:[J

iget-object v10, v1, Lcom/google/ctf/sandbox/ő$1;->this$0:Lcom/google/ctf/sandbox/ő;

iget v10, v10, Lcom/google/ctf/sandbox/ő;->ő:I

aget-wide v10, v9, v10

cmp-long v9, v7, v10

if-eqz v9, :cond_2a3

.line 76
iget-object v9, v1, Lcom/google/ctf/sandbox/ő$1;->val$textView:Landroid/widget/TextView;

const-string v10, "\u274c" ---> Bad boy ❌

invoke-virtual {v9, v10}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
```

Lastly, it checks that the variable `ő:I` has the same value than the length of the hashes array, which means that all the hashes are correct, and prints the good boy message.

```
iget-object v9, v1, Lcom/google/ctf/sandbox/ő$1;->this$0:Lcom/google/ctf/sandbox/ő;

iget v9, v9, Lcom/google/ctf/sandbox/ő;->ő:I

iget-object v10, v1, Lcom/google/ctf/sandbox/ő$1;->this$0:Lcom/google/ctf/sandbox/ő;

iget-object v10, v10, Lcom/google/ctf/sandbox/ő;->ő:[J

array-length v10, v10

if-lt v9, v10, :cond_2be

.line 82
iget-object v9, v1, Lcom/google/ctf/sandbox/ő$1;->val$textView:Landroid/widget/TextView;

const-string v10, "\ud83d\udea9" ---> Good boy 🚩

invoke-virtual {v9, v10}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
```

Also, in order to better understand the Smali code we debugged the APK with Android Studio and the Smalidea plugin using the steps of the following [post](https://medium.com/@ghxst.dev/static-analysis-and-debugging-on-android-using-smalidea-jdwp-and-adb-b073e6b9ae48) as a guide. 

To solve the hashes we created the following script in Python that bruteforces all the hashes with a specified charset:

```python
import struct
import string
import itertools

'''
Charsets
string.ascii_letters + '_!?{}' + string.digits
string.ascii_letters + '_'
'''

def pw_guess(charset):
    charset = string.ascii_letters + '_!?{}' + string.digits
    res = itertools.product(charset, repeat = 4)
    for guess in res:
        yield ''.join(guess)

def fibo_hash(a, b):
    if a == 0:
        result = [0] * 2
        result[0] = 0
        result[1] = 1
        return result
        
    else:
        temp = fibo_hash(b % a, a)
        
        final_result = [0] * 2
        v3 = temp[1]
        v5 = b // a
        v8 = temp[0]
        v5 = v5 * v8
        v3 = v3 - v5
        
        final_result[0] = v3 & 0xFFFFFFFF
        final_result[1] = temp[0] & 0xFFFFFFFF
        
        return final_result

flag_hash = [
            0x271986b, # We know it's 'CTF{'
            0xa64239c9,
            0x271ded4b,
            0x1186143,
            0xc0fa229f,
            0x690e10bf,
            0x28dca257,
            0x16c699d1,
            0x55a56ffd,
            0x7eb870a1,
            0xc5c9799f,
            0x2f838e65
            ]

default_charset = string.ascii_letters + '_!?{}' + string.digits     
flag = ''
for hash_to_crack in flag_hash:
    print('[+] Trying to crack 0x{:02x}'.format(hash_to_crack))
    if hash_to_crack == 0x55a56ffd:
        guess_generator = pw_guess(string.ascii_letters + '_')
    else:
        guess_generator = pw_guess(default_charset)
        
    for guess in guess_generator:
        if hash_to_crack == 0x271986b:
            guess = 'CTF{'
            
        char_value = struct.unpack("<I", guess.encode('utf-8'))[0]
        hash_result = fibo_hash(char_value, 0x100000000)
        
        result_set = frozenset(hash_result)
        if hash_to_crack in result_set:
            print('Hash 0x{:02x} cracked to: {}'.format(hash_to_crack, guess))
            flag += guess
            break

print('[+] Flag is: ', flag)
```

Python is very slow but if you run it with pypy3 and you set it to the maximal priority it doesn't take too long. Here we can see the output of the script.

```console
pypy3 solver.py
[+] Trying to crack 0x271986b
Hash 0x271986b cracked to: CTF{
[+] Trying to crack 0xa64239c9
Hash 0xa64239c9 cracked to: y0u_
[+] Trying to crack 0x271ded4b
Hash 0x271ded4b cracked to: c4n_
[+] Trying to crack 0x1186143
Hash 0x1186143 cracked to: k3ep
[+] Trying to crack 0xc0fa229f
Hash 0xc0fa229f cracked to: _y0u
[+] Trying to crack 0x690e10bf
Hash 0x690e10bf cracked to: ?_m4
[+] Trying to crack 0x28dca257
Hash 0x28dca257 cracked to: gic_
[+] Trying to crack 0x16c699d1
Hash 0x16c699d1 cracked to: 1_h4
[+] Trying to crack 0x55a56ffd
Hash 0x55a56ffd cracked to: Ue_l
[+] Trying to crack 0x7eb870a1
Hash 0x7eb870a1 cracked to: aser
[+] Trying to crack 0xc5c9799f
Hash 0xc5c9799f cracked to: _b3a
[+] Trying to crack 0x2f838e65
Hash 0x2f838e65 cracked to: ms!}
[+] Flag is:  CTF{y0u_c4n_k3ep_y0u?_m4gic_1_h4Ue_laser_b3ams!}
```

I also tried to use Z3 to solve the hashes but it crashed due to the recursion of the `fibo_hash` function.

```console
python3 z3_solver.py
Traceback (most recent call last):
  File "z3_solver_v2.py", line 12, in fibo_hash
    temp = fibo_hash(b % a, a)
  File "z3_solver_v2.py", line 12, in fibo_hash
    temp = fibo_hash(b % a, a)
  File "z3_solver_v2.py", line 12, in fibo_hash
    temp = fibo_hash(b % a, a)
  [Previous line repeated 987 more times]
  File "z3_solver_v2.py", line 5, in fibo_hash
    if a == 0:
ctypes.ArgumentError: argument 1: <class 'RecursionError'>: maximum recursion depth exceeded
```

So finally the flag is `CTF{y0u_c4n_k3ep_y0u?_m4gic_1_h4Ue_laser_b3ams!}`.

[1] Thanks to **@KaoRz** for pointing out that it’s the Extended Euclidean Algorithm.