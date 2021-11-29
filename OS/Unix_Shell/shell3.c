#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <wait.h>
#include <string.h>
#include <signal.h>
 
#define MAX_LINE 80     /* 80 chars per line, per command, should be enough. */
#define BUFFERSIZE 11
 
typedef struct{
    int number;
    char com[MAX_LINE];
}command;
 
command buffer[BUFFERSIZE];
int buffer_pointer;
int setup(char inputBuffer[], char *args[],int *background);
 
void print(){
    int i;
    fflush(stdout);
    write(STDOUT_FILENO,"\n",1);
    for(i = (buffer_pointer - 1) % BUFFERSIZE;\
        i != (buffer_pointer % BUFFERSIZE) && buffer[i].number;\
        i = (i - 1 + BUFFERSIZE) % BUFFERSIZE ){
        printf("%d\t%s",buffer[i].number,buffer[i].com);
        fflush(stdout);
    }
}
 
void handle_SIGINT(){    
    print();
    signal(SIGINT, SIG_IGN);
    return;
}
 
/**
 * setup() reads in the next command line, separating it into distinct tokens
 * using whitespace as delimiters. setup() sets the args parameter as a 
 * null-terminated string.
 */
int setup(char inputBuffer[], char *args[],int *background){
    int length, /* # of characters in the command line */
        i,      /* loop index for accessing inputBuffer array */
        start,  /* index where beginning of next command parameter is */
        ct;     /* index of where to place the next parameter into args[] */
    pid_t pid;
    ct = 0;
    length = read(STDIN_FILENO, inputBuffer, MAX_LINE);
    start = -1;
    if(length == 0)
        exit(0);            /* ^d was entered, end of user command stream */
    if(length < 0){
        //perror("error reading the command");
	    //exit(-1);           /* terminate with error code of -1 */
	    args[0] = NULL;
	    return 0;
    }        
    if(inputBuffer[0] == 'r' && (inputBuffer[1] == ' ' || inputBuffer[1] == '\n')){
        if(inputBuffer[1] == '\n'){        
            write(STDOUT_FILENO,buffer[(buffer_pointer - 1) % BUFFERSIZE].com,\
                                strlen(buffer[(buffer_pointer - 1) % BUFFERSIZE].com));
            strcpy(inputBuffer,buffer[(buffer_pointer - 1) % BUFFERSIZE].com);
            length = strlen(inputBuffer);
        }
        else{
            int j;
            if(!buffer_pointer) return 0;
            for(j = (buffer_pointer - 1) % BUFFERSIZE;\
                j != (buffer_pointer % BUFFERSIZE) && (buffer[j].com[0] != inputBuffer[2]) \
                                                   && buffer[j].number;\
                j = (j - 1 + BUFFERSIZE) % BUFFERSIZE );
            if(j == (buffer_pointer % BUFFERSIZE) || buffer[j].number == 0){
                char NF[15] = "Not found\n";
                write(STDOUT_FILENO,NF,strlen(NF));
                return 0;
            }
            else{
                write(STDOUT_FILENO,buffer[j].com,strlen(buffer[j].com));
                strcpy(inputBuffer,buffer[j].com);
                length = strlen(inputBuffer);
            }
        }
    }
    if(inputBuffer[0] != '\n'){
        buffer[(buffer_pointer % BUFFERSIZE)].number = buffer_pointer + 1;
        strcpy(buffer[(buffer_pointer % BUFFERSIZE)].com,inputBuffer);
        buffer_pointer++;
    }
    /* examine every character in the inputBuffer */
    for (i = 0;i < length;i++) { 
        switch (inputBuffer[i]){
	    case ' '  :
	    case '\t' :               /* argument separators */
		    if(start != -1){
                args[ct] = &inputBuffer[start];    /* set up pointer */
		        ct++;
		    }
            inputBuffer[i] = '\0'; /* add a null char; make a C string */
		    start = -1;
		    break;
        case '\n':                 /* should be the final char examined */
		    if (start != -1){
                args[ct] = &inputBuffer[start];     
		        ct++;
		    }
            inputBuffer[i] = '\0';
            args[ct] = NULL; /* no more arguments to this command */
		    break;
	    default :             /* some other character */
		    if (start == -1)
		        start = i;
            if (inputBuffer[i] == '&'){
		        *background  = 1;
                inputBuffer[i] = '\0';
		    }
	    } 
    }    
    args[ct] = NULL; /* just in case the input line was > 80 */
    return 1;
} 
 
int main(void){
 
    buffer_pointer = 0;
    memset(buffer, 0, sizeof(buffer));
    char inputBuffer[MAX_LINE]; /* buffer to hold the command entered */
    int background;             /* equals 1 if a command is followed by '&' */
    char *args[MAX_LINE/2 + 1];  /* command line (of 80) has max of 40 arguments */
    pid_t pid;
    char com[20] = " COMMAND->";
       
    while (1){            /* Program terminates normally inside setup */
	    background = 0;
	    memset(inputBuffer,0,MAX_LINE);
	    write(STDOUT_FILENO,com,strlen(com));
        setup(inputBuffer,args,&background);       /* get next command */       
        struct sigaction handler;
        handler.sa_handler = handle_SIGINT;
        sigaction(SIGINT,&handler,NULL);
	    /* the steps are:
	    (1) fork a child process using fork()
	    (2) the child process will invoke execvp()
	    (3) if background == 0, the parent will wait, 
		otherwise returns to the setup() function. */
		pid = fork();     
		if(pid < 0){
		    fprintf(stderr,"Fork Failed");
		    exit(-1);
		}
		else if(pid == 0){execvp(args[0],args);exit(0);}
		else if(!background) wait(NULL);
    }
    return 0;
}
 
 
 
 
 
 
 
 
 
 
 
 