#include <windows.h>
#include <iostream>

// Función para deshabilitar un privilegio en el token
bool DisablePrivilege(HANDLE tokenHandle, LPCWSTR privilege) {
    TOKEN_PRIVILEGES tokenPrivileges;
    LUID luid;

    if (!LookupPrivilegeValue(NULL, privilege, &luid)) {
        std::cerr << "Error al buscar el privilegio: " << GetLastError() << std::endl;
        return false;
    }

    tokenPrivileges.PrivilegeCount = 1;
    tokenPrivileges.Privileges[0].Luid = luid;
    tokenPrivileges.Privileges[0].Attributes = SE_PRIVILEGE_REMOVED;

    if (!AdjustTokenPrivileges(tokenHandle, FALSE, &tokenPrivileges, sizeof(TOKEN_PRIVILEGES), NULL, NULL)) {
        std::cerr << "Error al ajustar los privilegios del token: " << GetLastError() << std::endl;
        return false;
    }

    return true;
}

// Función para demostrar el manejo del modo de token efectivo
void DemonstrateEffectiveTokenMode() {
    HANDLE processToken;
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &processToken)) {
        std::cerr << "Error al abrir el token del proceso: " << GetLastError() << std::endl;
        return;
    }

    // Deshabilitar un privilegio (por ejemplo, SE_DEBUG_NAME)
    if (DisablePrivilege(processToken, SE_DEBUG_NAME)) {
        std::cout << "Privilegio SE_DEBUG_NAME deshabilitado." << std::endl;
    } else {
        CloseHandle(processToken);
        return;
    }

    // Simular el paso del token al servidor y verificar el privilegio deshabilitado
    HANDLE duplicateToken;
    if (!DuplicateTokenEx(processToken, TOKEN_ALL_ACCESS, NULL, SecurityImpersonation, TokenImpersonation, &duplicateToken)) {
        std::cerr << "Error al duplicar el token: " << GetLastError() << std::endl;
        CloseHandle(processToken);
        return;
    }

    // Aquí se simula la verificación en el servidor
    TOKEN_PRIVILEGES tokenPrivileges;
    DWORD tokenPrivilegesSize;
    if (GetTokenInformation(duplicateToken, TokenPrivileges, &tokenPrivileges, sizeof(TOKEN_PRIVILEGES), &tokenPrivilegesSize)) {
        for (DWORD i = 0; i < tokenPrivileges.PrivilegeCount; i++) {
            if (tokenPrivileges.Privileges[i].Luid.LowPart == SE_DEBUG_NAME) {
                if (tokenPrivileges.Privileges[i].Attributes & SE_PRIVILEGE_REMOVED) {
                    std::cout << "Privilegio SE_DEBUG_NAME permanece deshabilitado en el servidor." << std::endl;
                } else {
                    std::cout << "Privilegio SE_DEBUG_NAME habilitado en el servidor." << std::endl;
                }
            }
        }
    }

    CloseHandle(processToken);
    CloseHandle(duplicateToken);
}

int main() {
    DemonstrateEffectiveTokenMode();
    return 0;
