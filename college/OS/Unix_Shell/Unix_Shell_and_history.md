## OS_Ex

### Unix shell and history feature

#### reference

[unix-shell-and-history-feature/unix-shell.c at master · selmakahraman/unix-shell-and-history-feature · GitHub](https://github.com/selmakahraman/unix-shell-and-history-feature/blob/master/unix-shell.c)

[Unix-Shell-and-History-Feature/main.c at master · mohamed-minawi/Unix-Shell-and-History-Feature · GitHub](https://github.com/mohamed-minawi/Unix-Shell-and-History-Feature/blob/master/main.c)

[操作系统编程作业：UNIX Shell and History Feature_OrdinaryCrazy的博客-CSDN博客](https://blog.csdn.net/OrdinaryCrazy/article/details/80087193)

[操作系统第三章编程作业：UNIX Shell and History Feature_BIgData_Urumqi的博客-CSDN博客](https://blog.csdn.net/BIgData_Urumqi/article/details/108975649?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-2.essearch_pc_relevant&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-2.essearch_pc_relevant)



#### compile 

gcc -o myshell -lpthread myshell.c



#### problems

如果输入 !! 总是无法执行命令，因为把以前的命令拷贝到了一个局部数组中，无法保证一直存在。

execvp 会结束当前进程，所以要用子进程。

循环链表。

不能在子进程中修改要输出的变量！不然父进程不同步。



没搞懂 &
