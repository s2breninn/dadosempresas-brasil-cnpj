SELECT *
FROM Estabelecimentos AS E
    INNER JOIN Municipios AS M
        ON E.cd_municipio = M.cd_municipio