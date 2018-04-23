#include <iostream>
#include <mysql/mysql.h>

int main() {
  MYSQL *mysql = NULL;
  mysql_init(mysql);
  mysql_close(mysql);

  return 0;
}
