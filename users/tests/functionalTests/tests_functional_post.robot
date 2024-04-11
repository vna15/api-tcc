*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${base_url}    http://web:8000
${long_string}    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
${short_string}    aaaaaaaaaaaaa
${USERNAME}    admin
${PASSWORD}    admin

*** Test Cases ***
Teste de Criação de Usuário
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test@example.com    fullName=John Doe    CEP=12345678    age=30
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    201
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    email    test@example.com

Teste de Restrição de E-mail Único
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test@example.com    fullName=Jane Doe    CEP=87654321    age=25
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be True    ${response.status_code} in [400, 409]

Teste de Campos Obrigatórios na Criação de Usuário
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test2@example.com    # Missing required fields
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    400

Criar Novo Usuário - E-mail Duplicado
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test3@example.com    fullName=John Doe    CEP=12345678    age=30
    ${response1}    Post Request    Users    /user/    json=${data}    headers=${headers}
    ${data}    Create Dictionary    email=test3@example.com    fullName=Jane Doe    CEP=87654321    age=25
    ${response2}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be True    ${response2.status_code} in [400, 409]

Tentar Criar Usuário com CEP Inválido
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test4@example.com    fullName=John Doe    CEP=abc123    age=30  # Invalid CEP format
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    400

Verificar Limite de Caracteres no Campo de E-mail
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=${long_string}@example.com    fullName=John Doe    CEP=12345678    age=30  # Exceeds maximum length
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be True    ${response.status_code} in [400, 422]

Verificar Limite de Caracteres no Campo de Nome Completo
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test5@example.com    fullName=${long_string}    CEP=12345678    age=30  # Exceeds maximum length
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be True    ${response.status_code} in [400, 422]

Verificar Limite de Caracteres no Campo de CEP
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test6@example.com    fullName=John Doe    CEP=123456789    age=30  # Exceeds maximum length
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be True    ${response.status_code} in [400, 422]

Verificar Limite de Caracteres no Campo de Telefone Celular
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test7@example.com    fullName=John Doe    CEP=12345678    age=30    cellPhone=${short_string}  # Exceeds maximum length
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be True    ${response.status_code} in [400, 422]

Verificar Valor Negativo no Campo de Idade
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test8@example.com    fullName=John Doe    CEP=12345678    age=${-20}  # Negative value
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be True    ${response.status_code} in [400, 422]

Deletar Usuário 1
    [Template]    Deletar Usuário
    test@example.com

Deletar Usuário 2
    [Template]    Deletar Usuário
    test3@example.com

*** Keywords ***
Deletar Usuário
    ${TOKEN}=   Obter token
    [Arguments]    ${email}
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=${email}
    ${response}    Delete Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    204
    
Obter token
    Create Session    Users    ${base_url}
    ${data}=    Create Dictionary    username=${USERNAME}    password=${PASSWORD}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${response}=    Post Request   Users     ${BASE_URL}/token/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    200
    ${TOKEN}=    Set Variable    Bearer ${response.json()["access"]}
    RETURN      ${TOKEN}