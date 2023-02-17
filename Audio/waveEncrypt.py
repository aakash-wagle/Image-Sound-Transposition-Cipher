import math
import wave
# import os

def encryptAudio(obj, key, chunkSize=5000):
	frames = obj.readframes(-1)
	keyLen = len(key)
	numFrames = len(frames)
	matrix = {}
	step =  keyLen # keyLen*chunkSize
	colLength = math.ceil(numFrames/step)
	key = list(key)
	for i, colNumber in enumerate(key):
		matrix[colNumber] = bytearray([frames[x] for x in range(i, numFrames, step)])
		if len(matrix[colNumber])<colLength:
			temp = bytearray(colLength-len(matrix[colNumber]))
			matrix[colNumber].extend(temp)
	key = sorted(key)
	newFrames = bytearray()
	for colNumber in key:
		newFrames.extend(matrix[colNumber])
	
	# Creating new audio file and setting required parameters
	filename = "encrypted.wav"
	newObj = wave.open("encrypted.wav", 'wb')
	newObj.setnchannels(obj.getnchannels())
	newObj.setsampwidth(obj.getsampwidth())
	newObj.setframerate(obj.getframerate())
	newObj.writeframes(newFrames)
	newObj.close()
	return filename
	
def decryptAudio(obj, key):
	frames = obj.readframes(-1)
	keyLen = len(key)
	numFrames = len(frames)

	matrix = {}
	matrixKeys = sorted([x for x in key])
	step =  keyLen # keyLen*chunkSize
	colLength = math.ceil(numFrames/step)

	temp = bytearray()
	for i, frame in enumerate(frames):
		temp.append(frame)
		if((i+1)%colLength==0):
			matrix[matrixKeys[i//colLength]] = temp
			temp = []
	
	newFrames = bytearray()
	for i in range(0, colLength):
		for colNumber in key:
			newFrames.append(matrix[colNumber][i]) 

	filename = "decrypted.wav"
	newObj = wave.open(filename, 'wb')
	newObj.setnchannels(obj.getnchannels())
	newObj.setsampwidth(obj.getsampwidth())
	newObj.setframerate(obj.getframerate())
	newObj.writeframes(newFrames)
	newObj.close()
	return filename

if __name__=="__main__":
	print("Alice's Side")
	src = "plainaudiofile.wav"
	# key = "game"
	key = input("Enter the encryption key: ")
	obj = wave.open(src, "rb")
	fName = encryptAudio(obj, key)
	print("Encrypted audio generated.\nFilename:", fName)
	obj.close()

	print("\nBob's Side")
	src = fName
	obj = wave.open(src, "rb")
	decryptAudio(obj, key)
	fName = print("Encrypted audio generated.\nFilename:", fName)
	obj.close()


	# print(os.path.abspath(src))
	# key = "game"
	# print("Number of channels:", obj.getnchannels())
	# print("Sample width:", obj.getsampwidth())
	# print("Frame Rate:", obj.getframerate())
	# print("Number of frames:", obj.getnframes())
	# print("Parameters:", obj.getparams())
	# audioTime = obj.getnframes()/obj.getframerate()
	# print("Time:", audioTime)

	# print(len(frames)/4) This is the same as obj.getnframes()
	# print(len(frames)/4)