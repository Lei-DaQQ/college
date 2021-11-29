#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <sys/types.h>
#include <wait.h>
#define MAX_LINE 80

#define MAX_CMDS_CNT 10

typedef struct History {
	char command_line[MAX_LINE];
	int usage_cnt; //此程序为用到该变量
} history;

history h_lst[MAX_CMDS_CNT];

int head = 0, tail = 0;
// head指向链表首部，tail指向链表尾部的下一个编号
//故判断Head和tail的值，可以得出链表是否为空。

int cmd_cnt = 0;

int should_run = 1;


void save_command(char *command_buffer)
{
	/*
	//可以注释是因为 空表 和不空表的操作一样。不过 usage_cnt这里赋值为1更严谨，
	但是结构体里默认值为0，所以就直接usage_cnt++
	// empty list:
	if(head == tail) {
		strcpy(h_lst[tail].command_line, command_buffer);
		h_lst[tail].usage_cnt ++;
		tail++; // tail = (tail + 1) % MAX_CMDS_CNT
		return ;
	}
	*/

//是否不空，且和上一条命令完全相同(输入的串完全相同)
	int indx = (tail - 1 + MAX_CMDS_CNT) % MAX_CMDS_CNT;
	// 加MAX_CMDS_CNT, 防止tail = 0时， tail - 1 = -1，负数索引
	if (head != tail && strcmp(command_buffer, h_lst[indx].command_line) == 0) {
		h_lst[indx].usage_cnt++;
		return ;
	}

	strcpy(h_lst[tail].command_line, command_buffer);
	h_lst[tail].usage_cnt ++;
	tail = (tail + 1) % MAX_CMDS_CNT;
	if(tail == head) head ++;//覆盖链表首部

	cmd_cnt++;
	// printf("cmd_cnt: %d \n", cmd_cnt);
}

void delete_last_elem()
{
	if(head == tail)
		return ;
	tail = (tail - 1 + MAX_CMDS_CNT) % MAX_CMDS_CNT;
	cmd_cnt --;
}

void display_commands_history()
{
	if(head == tail) {
		printf("No commands in history.\n");
		return ;
	}

	//从链尾，往链首遍历
	int i = tail -1;
	int endi = (head - 1 + MAX_CMDS_CNT) % MAX_CMDS_CNT;
	int t_cnt = cmd_cnt;
	while(i != endi) {
		printf("%3d %s\n", t_cnt--, h_lst[i].command_line);
		i = (i - 1 + MAX_CMDS_CNT) % MAX_CMDS_CNT;
	}
}


int process_command(char command_buffer[], char *args[], int *background)
{
	// printf("com_buffer:%s\n", command_buffer );
	save_command(command_buffer);
	//if it is !! or !N, latter program will change the command_line.


	char *delim = " \r\t\n";

	int tcnt = 0;
	args[tcnt++] = strtok(command_buffer, delim);
	// printf("%s \n", args[tcnt-1]);

	while( args[tcnt++] = strtok(NULL, delim)) ;
	// 注意这个while的分号
	// printf("args count: %d\n", tcnt);
	//now args[tcnt-1] == NULL, it's ok.
	// if(args[tcnt-1] == NULL){
	// printf("args[] is NULL!\n");
	// }

	// printf("%s\n", args[tcnt-1]);
	if(args[tcnt-2][0] == '&') {
		args[tcnt-2] = NULL;
		*background = 1;
	}
	//处理结束，接下来执行命令，在主函数进行


	if(strcmp(args[0], "!!") == 0 && args[1] == NULL) {
		delete_last_elem();
		if(cmd_cnt == 0) {
			printf("No commands in history!\n");
			return 0;
		} else {
			// char new_cmd_buffer[MAX_LINE];

			int indx = (tail - 1 + MAX_CMDS_CNT) % MAX_CMDS_CNT;
			// strcpy(new_cmd_buffer, h_lst[indx].command_line);
			strcpy(command_buffer, h_lst[indx].command_line);

			// printf("last cmd: %s\n", new_cmd_buffer);
			// printf("args[0]: %s\n", args[0]);
			// if(args[1] == NULL){
			// printf("args1 == NULL\n");
			// }
			// return process_command(new_cmd_buffer, args, background);
			return process_command(command_buffer, args, background);
		}
	}

	// N should [cmd_cnt - MAX_CMDS_CNT + 1, cmd_cnt] and > 0.
	if(args[0][0] == '!' && args[1] == NULL) {
		delete_last_elem();

		int is_int = 1;
		for(int j = 1; args[0][j]; ++j) {
			if(!isdigit(args[0][j])) {
				is_int = 0;
				break;
			}
		}
		if(is_int) {

			int ret_n = atoi(&args[0][1]);

			int min_cmd_ind = 1 > cmd_cnt - MAX_CMDS_CNT + 1 ? 1 : cmd_cnt - MAX_CMDS_CNT + 1;
			int max_cmd_ind = cmd_cnt;

			if( ! (ret_n >= min_cmd_ind && ret_n <= max_cmd_ind) ) {
				printf("No such command in history.\n");
				return 0;
			}

			int offset = (cmd_cnt - ret_n);
			int indx = (tail - 1 - offset + MAX_CMDS_CNT) % MAX_CMDS_CNT;

			// char new_cmd_buffer[MAX_LINE];
			strcpy(command_buffer, h_lst[indx].command_line);
			// strcpy(new_cmd_buffer, h_lst[indx].command_line);
			// return process_command(new_cmd_buffer, args, background);
			return process_command(command_buffer, args, background);

		}

	}
	if (strcmp(args[0], "exit") == 0 && args[1] == NULL) {
		should_run = 0;
	} else if (strcmp(args[0], "history") == 0 && args[1] == NULL) {
		delete_last_elem();
	}
	return 1;

}


int get_command(char command_buffer[], char *args[], int *background)
{

	int length;
	length = read(STDIN_FILENO, command_buffer, MAX_LINE);
	if (length == 1) // \n
		return 0;

	if (length < 0) {
		printf("Command reading failure!\n");
		exit(-1);
	}

	command_buffer[length-1] = 0;
	return process_command(command_buffer, args, background);
}


int execute_command(char *args[], int *background)
{
	if (strcmp(args[0], "history") == 0) {
		display_commands_history();
		return 1;
	}
	if(strcmp(args[0], "exit") == 0) {
		exit(0);
	}
	execvp(args[0], args);

}



int main(int argc, char *argv[])
{



	char command_buffer[MAX_LINE];
	int background;
	char *args[MAX_LINE / 2 + 1];

	pid_t pid, tpid;

	while (should_run) {

		background = 0;
		printf("osh>");
		fflush(stdout);

		int ret_flag = get_command(command_buffer, args, &background);
		if (ret_flag > 0) {
			pid = fork();

			if (pid < 0) {
				printf("Failed to fork a process!\n");
				exit(1);
			} else if (pid == 0) {
				//child process
				if (execute_command(args, &background) == -1)
					printf("Failed to execute the command!\n");
				break;
			} else {
				// father process
				if (background == 0) {
					wait(NULL);
				}
			}
		}
	}
	return 0;
}