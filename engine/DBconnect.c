#include <stdio.h>
#include <mysql/mysql.h>

int main()
{
	MYSQL conexao;

	mysql_init(&conexao);
	if( mysql_real_connect(&conexao, "localhost", "coolbaguser", "m1cr0@t805i", "coolbag", 0, NULL, 0) )
	{
		printf("conectado com sucesso!\n");
		mysql_close(&conexao);
	}
	else
	{
		printf("Falha de conexao\n");
		printf("Erro %d : %s\n", mysql_errno(&conexao), mysql_error(&conexao));
	}
return 0;
}