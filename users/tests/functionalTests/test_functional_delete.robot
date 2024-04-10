*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${base_url}    http://web:8000

*** Test Cases ***
Teste de Deleção de Usuário
    [Documentation]    Verificar se um usuário pode ser excluído com sucesso.
    Criar Usuário
    Create Session    Users    ${base_url}
    ${email}    Set Variable    test@example.com
    ${headers}    Create Dictionary    Content-Type=application/json
    ${data}    Create Dictionary    email=${email}
    ${response}    Delete Request    Users    /user/    json=${data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    204

Tentar Deletar Usuário com E-mail Inexistente
    [Documentation]    Verificar se o sistema trata adequadamente tentativas de exclusão de um usuário com um e-mail que não existe no sistema.
    Create Session    Users    ${base_url}
    ${updated_data}    Create Dictionary    email=update@teste.com    fullName=John Doe    CEP=12345678    age=30    # Defina os dados atualizados do usuário
    ${headers}    Create Dictionary    Content-Type=application/json
    ${response}    Put Request    Users    /user/    json=${updated_data}    headers=${headers}
    Should Be Equal As Strings    ${response.status_code}    404    # Verifica se o código de status é 404 Not Found
    ${json}    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    error    User not found    # Verifica se a mensagem de erro é correta

*** Keywords ***
 Criar Usuário
     Create Session    Users    ${base_url}
     ${headers}    Create Dictionary    Content-Type=application/json
     ${data}    Create Dictionary    email=test@example.com    fullName=John Doe    CEP=12345678    age=30
     ${response}    Post Request    Users    /user/    json=${data}    headers=${headers}
     Should Be Equal As Strings    ${response.status_code}    201
     ${json}    Set Variable    ${response.json()}
     Dictionary Should Contain Key    ${json}    email    test@example.com