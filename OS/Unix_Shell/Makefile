cc = gcc

filename = myshell

src1 = $(filename).c
out = $(filename)

$(out): $(src1)
	$(cc)  -std=c99 -lpthread -o $(out) $(src1)

run:
	./$(out)

clean:
	rm -rf $(out)
