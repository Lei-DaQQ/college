#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/wait.h>

// Constants
#define MAX_ARG 15
#define MAX_LINE 80
#define MAX_HISTORY 10

// Functions Prototype
char * inputtext();
char ** parsetext(char * input);
char ** executeshell(char * instruction);
void execute(char *arg, char **args);
void historyfeature(char * instruction,int featurenum);
char* returninstruction(int x);

//Global Variable and Arrays used for program
int sizeofcmd, numarg=0, currenthistory=-1;
char running = 1, tempbool=0, bls=0, ready=0;
char * history[MAX_HISTORY];
char **cmdpnt;

// Main Program
int main()
{
	char * input;
	int i;
	char ** commands;
	// Loop running the program
	while(running) {
		input = inputtext();
		if(input[0]!='\n') {
			input = strtok(input,"\n\r");
			commands  = executeshell(input);
			// Executing the commands
			if(ready) {
				execute(commands[0],commands);

				ready=0;
				free(commands);

			}

			if(bls)
				free(cmdpnt),bls=0;

			numarg = 0;


		}

	}

	return 0;
}

// Function that inputs the whole instruction
char * inputtext()
{
	char *buffer = NULL;
	size_t x;
	printf("MitchoCMD> ");
	fflush(stdout);
	sizeofcmd = getline(&buffer, &x, stdin);
	if(sizeofcmd == -1 && sizeofcmd < MAX_LINE)
		printf("Error Reading the Line \n");
	return buffer;
}

// Function that tokenizes the instruction into several independent words
char ** parsetext(char * input)
{
	char **cmd;
	cmd = malloc(MAX_ARG* sizeof(char *));
	char *temp;
	temp = strtok(input," \t\r\a\n");
	while(temp != NULL && numarg<=MAX_ARG) {
		cmd[numarg++]=temp;
		temp = strtok(NULL, " \t\r\a\n");
	}

	return cmd;
}

// Function Responsible for the shell events
char ** executeshell(char * instruction)
{
	char *tempstring = malloc((strlen(instruction))*sizeof(char));
	strcpy(tempstring,instruction);

	char ** commands  = parsetext(tempstring);
	if(commands[0] != NULL) {
		if(!strcmp(commands[0], "history"))
			free(tempstring),historyfeature(instruction,0),ready=0;
		else if(!strcmp(commands[0], "!!"))
			free(tempstring), historyfeature(instruction,1),ready=0;

		else if(commands[0][0]=='!' && isdigit(commands[0][1]))
			free(tempstring), historyfeature(instruction,2),ready=0;
		else if(!strcmp(commands[0], "exit"))
			running=0, ready=0;
		else {
			historyfeature(instruction,3);
			ready=1;
		}
	}
	return commands;

}

// Function that executes the commands using forks
void execute(char *arg, char **args)
{

	if (!strcmp(args[numarg-1],"&"))    // Concurrency Test
		tempbool=1, args[numarg-1]=NULL;

	pid_t pid= fork();

	if (pid < 0) {                 // Fork Failure
		fprintf(stderr, "Fork Failed\n");

	} else if (pid == 0) {          // Fork Success Child
		if(execvp(arg,args)==-1) {
			printf("Invalid Command\n");
			exit(0);
		}
	} else {                 // Parent
		if(tempbool)
			wait(NULL), tempbool=0;
	}


}

// Function responsible for the history
void historyfeature(char * instruction, int featurenum)
{


	int i;
	char * tempstring;
	if(featurenum==0) {      // Printing the history
		if(currenthistory !=-1) {
			for(i=0; i<currenthistory+1; i++)
				printf("%d: %s \n",i,history[i]);
		} else printf("No Commands in History 0\n");
	}

	else if(featurenum==1) {      // !! Functionality
		if(currenthistory !=-1) {
			tempstring = returninstruction(currenthistory);
			numarg = 0;
			cmdpnt = parsetext(tempstring);
			execute(cmdpnt[0],cmdpnt);
			free(tempstring);
			bls=1;
		} else printf("No Commands in History 1\n");

	}

	else if(featurenum==2) {      // !digit Functionality
		if(currenthistory !=-1) {
			int x =instruction[1]-'0';

			if(x>=0 && x<=currenthistory) {
				tempstring = returninstruction(x);
				numarg = 0;
				cmdpnt = parsetext(tempstring);
				execute(cmdpnt[0],cmdpnt);
				free(tempstring);
				bls=1;

			} else printf("No Such Commands in History\n");
		} else printf("No Commands in History 2\n");
	}

	else if(featurenum==3) {  // Saving in history functionality
		if(currenthistory!=MAX_HISTORY-1) {
			currenthistory=currenthistory +1;
			history[currenthistory] = instruction;
		} else if(currenthistory==MAX_HISTORY-1) {
			int x;
			for(x=1; x<MAX_HISTORY; x++)
				history[x-1] = history[x];
			history[MAX_HISTORY-1] = instruction;
		}

	}


}

// Function that returns the instruction from the history
char* returninstruction(int x)
{
	char *tempstring = malloc((strlen(history[x]))*sizeof(char));
	strcpy(tempstring,history[x]);
	return tempstring;

}