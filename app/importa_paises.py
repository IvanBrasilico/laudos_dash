
lista_paises = []
with open('./paises.txt', 'rt') as paises:
    for linha in paises:
        codigo = linha.strip()
        nome = next(paises).strip()
        # print('*', codigo, '*', '"', nome, '"')
        lista_paises.append((codigo, nome))

print(lista_paises)


with open('./paises.sql', 'wt') as paises_out:
    paises_out.write(
        'CREATE TABLE paises (' +
        '`id` bigint(20) NOT NULL AUTO_INCREMENT,' +
        '`codigo` bigint(20) NOT NULL,' +
        '`dataregistro` datetime DEFAULT NULL,' +
        '`username` varchar(20) DEFAULT NULL, , ' +
        '`nome` varchar(50) DEFAULT NULL, ' +
        'PRIMARY KEY(`id`),' +
        ') ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = latin1;\n'
    )
    for linha in lista_paises:
        paises_out.write(
            'INSERT INTO paises (ID, codigo, nome)' +
            'VALUES ({}, {}, "{}")'.format(linha[0], linha[0], linha[1]) + ';\n')
