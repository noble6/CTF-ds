#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_NOTES 8
#define MAX_SIZE 0x80

typedef struct {
    char *content;
    size_t size;
    int in_use;
} Note;

Note *notes[MAX_NOTES];
int note_count = 0;

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    memset(notes, 0, sizeof(notes));
}

void read_str(char *buf, size_t size) {
    ssize_t n = read(0, buf, size - 1);
    if (n > 0 && buf[n-1] == '\n') {
        buf[n-1] = '\0';
    }
}

int read_int() {
    char buf[16];
    read_str(buf, sizeof(buf));
    return atoi(buf);
}

void menu() {
    puts("\n=== Heap Roulette ===");
    puts("1. Create note");
    puts("2. Edit note");
    puts("3. Delete note");
    puts("4. View note");
    puts("5. Exit");
    printf("> ");
}

int find_free_slot() {
    for (int i = 0; i < MAX_NOTES; i++) {
        if (!notes[i]) return i;
    }
    return -1;
}

void create_note() {
    int idx = find_free_slot();
    if (idx == -1) {
        puts("No free slots!");
        return;
    }
    
    printf("Size: ");
    size_t size = read_int();
    
    if (size > MAX_SIZE || size == 0) {
        puts("Invalid size!");
        return;
    }
    
    notes[idx] = malloc(sizeof(Note));
    notes[idx]->content = malloc(size);
    notes[idx]->size = size;
    notes[idx]->in_use = 1;
    
    printf("Content: ");
    read_str(notes[idx]->content, size);
    
    printf("Created note %d\n", idx);
}

void edit_note() {
    printf("Index: ");
    int idx = read_int();
    
    if (idx < 0 || idx >= MAX_NOTES || !notes[idx]) {
        puts("Invalid index!");
        return;
    }
    
    printf("New content: ");
    read(0, notes[idx]->content, notes[idx]->size + 1);
    
    puts("Updated!");
}

void delete_note() {
    printf("Index: ");
    int idx = read_int();
    
    if (idx < 0 || idx >= MAX_NOTES || !notes[idx]) {
        puts("Invalid index!");
        return;
    }
    
    free(notes[idx]->content);
    
    notes[idx]->in_use = 0;
    
    puts("Deleted!");
}

void view_note() {
    printf("Index: ");
    int idx = read_int();
    
    if (idx < 0 || idx >= MAX_NOTES || !notes[idx]) {
        puts("Invalid index!");
        return;
    }
    
    printf("Content: %s\n", notes[idx]->content);
    printf("Size: %zu\n", notes[idx]->size);
}

void secret_function() {
    system("/bin/sh");
}

int main() {
    init();
    
    puts("=============================");
    puts("  Heap Roulette v2.0");
    puts("  College CTF 2026");
    puts("=============================");
    puts("");
    puts("Can you corrupt the heap and get a shell?");
    puts("");
    
    while (1) {
        menu();
        int choice = read_int();
        
        switch (choice) {
            case 1: create_note(); break;
            case 2: edit_note(); break;
            case 3: delete_note(); break;
            case 4: view_note(); break;
            case 5: puts("Bye!"); exit(0);
            default: puts("Invalid choice!");
        }
    }
    
    return 0;
}
