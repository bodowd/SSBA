#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

#define STACK_SIZE 65536

struct child_config {
  int argc;
  char **argv;
  char *hostname;
};

/* Entry point for child after `clone` */
int child(void *arg) {
  struct child_config *config = arg;
  sethostname(config->hostname, strlen(config->hostname));
  if (execvpe(config->argv[0], config->argv, NULL)) {
    fprintf(stderr, "execvpe failed %m.\n");
    return -1;
  }

  return 0;
}

int main(int argc, char **argv) {
  struct child_config config = {0};
  int flags = CLONE_NEWNET | SIGCHLD | CLONE_NEWNS | CLONE_NEWCGROUP |
              CLONE_NEWPID | CLONE_NEWIPC | CLONE_NEWUTS;
  pid_t child_pid = 0;

  // Prepare child configuration
  config.argc = argc - 1;
  config.argv = &argv[1];

  // Allocate stack for child
  char *stack = 0;
  if (!(stack = malloc(STACK_SIZE))) {
    fprintf(stderr, "Malloc failed");
    exit(1);
  }

  char hostname[256] = {0};
  snprintf(hostname, 256, "%s", "ssba");
  config.hostname = hostname;

  // Clone parent, enter child code

  // https://www.redhat.com/sysadmin/mount-namespaces
  // explored CLONE_NEWNS to create a new mount namespace. This will
  // still initialize the child mount namespace with the parent's, but
  // new namespaces made in the child will not be seen in the parent
  // ex: (inside container) mount -t tmpfs tmpfs /mnt
  // findmnt | grep mnt
  // returns something with /mnt, tmpfs, tmpfs,...
  // running findmnt|grep mnt in the host, there will be nothing returned
  if ((child_pid = clone(child, stack + STACK_SIZE, flags, &config)) == -1) {
    fprintf(stderr, "Clone failed");
    exit(2);
  }

  // mkdir("/sys/fs/cgroup/pids")

  wait(NULL);

  return 0;
}
