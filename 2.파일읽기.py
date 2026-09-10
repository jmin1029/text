""" with open("memo.txt","r",encoding="utf-8")as file:
	content=file.read()

print(content)


with open("memo.txt","r",encoding="utf-8")as file:
	line1=file.readline()
	line2=file.readline()

print(line1)
print(line2)
 """
with open("memo.txt","r",encoding="utf-8")as file:
	lines=file.readlines()
 #여러줄을 읽을 수 있다.


with open("memo.txt","a",encoding="utf-8")as file:
	lines= lines + file.write("4일차 학습\n") 
 
 
print(lines)

#리스트 반복문으로 끌어오기 가능
for line in lines:
	print(line.strip()) 