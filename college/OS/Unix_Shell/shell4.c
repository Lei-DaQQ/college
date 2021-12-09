#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include <stdlib.h>


#define MAX_LINE 80

int length(int a[])
{
	int n=0;
	while(a[n]!='\0')   n++;  //'\0'=>表示的是数组存放元素结束的标志
	return n;
}

int main()
{
	char *args[MAX_LINE][MAX_LINE];//={"ps","-ael","NULL"};
	int should_run = 1;
	int i = 0;
	int j = 0;
	int his_i = 1;
	//char *his1[MAX_LINE];
	//char *his2[MAX_LINE];
	//char *doublehis[MAX_LINE][MAXLINE];
	for(i=0; i<MAX_LINE; i++) {
		//args[i] = (char*)malloc(20*sizeof(char));
		//his1[i] = (char*)malloc(20*sizeof(char));
		//his2[i] = (char*)malloc(20*sizeof(char));
		for(j=0; j<MAX_LINE; j++) {
			args[i][j] = (char*)malloc(20*sizeof(char));
		}
	}
	while(should_run) {
		if(strcmp(args[his_i-1][0],"!!") == 0) {
			if(his_i-2>0) {
				for(i=0; i<5; i++) {
					args[his_i][i] = args[his_i-2][i];
				}
			} else {
				printf("No command in history!\n");
				i=0;
				printf("osh>");
				//int len = read(0, string, 20);
				//setup(string,args,&b);
				do {
					scanf("%s",args[his_i][i]);
					i++;
				} while(getchar() != '\n');
				args[his_i][i] = NULL;
			}
		} else {
			i=0;
			printf("osh>");
			//int len = read(0, string, 20);
			//setup(string,args,&b);
			do {
				scanf("%s",args[his_i][i]);
				i++;
			} while(getchar() != '\n');
			args[his_i][i] = NULL;
		}

		//his1[his_i] = args[0];
		//his2[his_i] = args;

		//for(i=0;i<his_i;i++){
		//printf("%d %s\n",i+1,his1[i]);
		//}
		pid_t pid;
		pid = fork();
		if(pid < 0) {
			fprintf(stderr,"Fork Failed");
			return 1;
		} else if(pid == 0) {
			// execlp("/bin/ls","ls",NULL);
			if(strcmp(args[his_i][0],"exit") == 0) {
				should_run = 0;
				exit(0);
				return 0;
			} else if(strcmp(args[his_i][0],"history") == 0) {
				for(i=his_i; (i>0)&&(i>his_i-10); i--) {
					printf("%d--%s\n",i,args[i][0]);
				}

			} else if(strcmp(args[his_i][0],"!!") == 0) {
				his_i++;
				continue;
				//char *temp[10] = {"history",0};
				//int id1 = execvp(args[his_i-1][0],args[his_i-1]);
				// int id1 = execvp(temp[0],temp);
				// if(id1 < 0){
				//     //printf("%d-%s-%s",id1,args[his_i-1][0],args[his_i-1][1]);
				//     printf("Not find command!\n");
				// }
			} else {
				int id = execvp(args[his_i][0],args[his_i]);
				//int id = execvp(*his[his_i-1],his[his_i-1]);
				if(id < 0) {
					printf("Not find command!\n");
				}
			}
			//printf("%d   I am child   %d\n",getpid(),getppid());
		} else {
			if(args[his_i][strlen(args[his_i])-3]=="&") {
				continue;
			} else {
				wait(NULL);
			}

		}
		his_i++;
		fflush(stdout);
	}
	for(i=0; i<MAX_LINE; i++) {
		//args[i] = (char*)malloc(20*sizeof(char));
		//his[i] = (char*)malloc(20*sizeof(char));
		for(j=0; j<MAX_LINE; j++) {
			free(args[i][j]);
		}

		//free(his1[i]);
		//free(his2[i]);
	}
	return 0;
}
