#General C/C++ Makefile.

#Target
TARGET = test_filter


#Directories
SRC_DIR=src
OBJ_DIR = obj
RUN_DIR = run

#Compilers
CC = gcc
CXX = g++	

C_FILES=$(wildcard $(SRC_DIR)/*.c)
CXX_FILES=$(wildcard $(SRC_DIR)/*.cpp)
OBJS_C= $(addprefix $(OBJ_DIR)/,$(notdir $(patsubst %.c,%.o,$(C_FILES))))
OBJS_CXX= $(addprefix $(OBJ_DIR)/,$(notdir $(patsubst %.cpp,%.o,$(CXX_FILES))))
OBJS = $(OBJS_C) $(OBJS_CXX)


#Rules
all: $(RUN_DIR)/$(TARGET).run 

$(RUN_DIR)/$(TARGET).run: $(OBJS)
	$(CXX) -g $^ -o $@

.PRECIOUS: $(OBJ_DIR)/%.o
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) -c $^ -o $@

.PRECIOUS: $(OBJ_DIR)/%.o
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) -c $^ -o $@

clean:
	rm -rf $(OBJ_DIR)/*
	rm -rf $(RUN_DIR)/*



