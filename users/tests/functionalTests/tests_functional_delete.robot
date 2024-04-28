*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${base_url}    http://web:8000
${USERNAME}    admin
${PASSWORD}    admin

*** Test Cases ***
Teste de Deleção de Usuário
    [Documentation]    Verificar se um usuário pode ser excluído com sucesso.
    ${TOKEN}=   Obter token
    Criar Usuário
    Create Session    Users    ${base_url}
    ${email}    Set Variable    test@example.com
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=${email}
    ${response}    Delete Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    204

Tentar Deletar Usuário com E-mail Inexistente
    [Documentation]    Verificar se o sistema trata adequadamente tentativas de exclusão de um usuário com um e-mail que não existe no sistema.
    ${TOKEN}=   Obter token
    Criar Usuário
    Create Session    Users    ${base_url}
    ${email}    Set Variable    test@example.com
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=${email}
    ${response}    Delete Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    404   # Verifica se o código de status é 404 Not Found
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    error    User not found    # Verifica se a mensagem de erro é correta

*** Keywords ***
Criar Usuário
    ${TOKEN}=   Obter token
    Create Session    Users    ${base_url}
    ${headers}=    Create Dictionary    Authorization=${TOKEN}    Content-Type=application/json
    ${data}    Create Dictionary    email=test@example.com    fullName=John Doe    CEP=12345678    age=30
    ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    201
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    email    test@example.com

Obter token
    Create Session    Users    ${base_url}
    ${data}=    Create Dictionary    username=${USERNAME}    password=${PASSWORD}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${response}=    Post Request   Users     ${BASE_URL}/token/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    200
    ${TOKEN}=    Set Variable    Bearer ${response.json()["access"]}
    RETURN      ${TOKEN}