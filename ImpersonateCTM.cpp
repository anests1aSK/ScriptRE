#include <windows.h>
#include <iostream>

void CheckThreadToken() {
    HANDLE tokenHandle = NULL;
    if (OpenThreadToken(GetCurrentThread(), TOKEN_QUERY, TRUE, &tokenHandle)) {
        std::cout << "Token abierto. El hilo está impersonando a otro usuario." << std::endl;
        // Aquí se puede hacer más procesamiento con el token
        CloseHandle(tokenHandle);
    } else {
        std::cout << "No se pudo abrir el token del hilo. Error: " << GetLastError() << std::endl;
    }
}

int main() {
    // Simulación de impersonación
    // ImpersonateLoggedOnUser(tokenDeImpersonacion);

    // Chequeo del token del hilo
    CheckThreadToken();

    return 0;
