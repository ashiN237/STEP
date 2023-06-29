//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  metadata->next = my_heap.free_head;
  my_heap.free_head = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}


// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  my_metadata_t *best_fit_metadata = NULL;
  my_metadata_t *best_fit_prev = NULL;
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;

  // 最適なスロットを見つける(best-fit)
  while (metadata) {
    if (metadata->size >= size && (!best_fit_metadata || metadata->size < best_fit_metadata->size)) {
      best_fit_metadata = metadata;
      best_fit_prev = prev;
      if (metadata->size == size)
        break; // Found an exact match
    }
    prev = metadata;
    metadata = metadata->next;
  }

  if (!best_fit_metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    my_add_to_free_list(metadata);
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = best_fit_metadata + 1;
  size_t remaining_size = best_fit_metadata->size - size;
  my_remove_from_free_list(best_fit_metadata, best_fit_prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    my_add_to_free_list(new_metadata);
    best_fit_metadata->size = size;
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;

  // 空きスロットを空きリストに追加
  my_add_to_free_list(metadata);

  // 隣接する空きスロットがある場合はそれを結合
  my_metadata_t *prev_metadata = NULL;
  my_metadata_t *curr_metadata = my_heap.free_head;
  while (curr_metadata) {
    // 現在のメタデータと次のメタデータがメモリ上で隣接しているかどうかをチェック
    if ((char *)curr_metadata + curr_metadata->size + sizeof(my_metadata_t) == (char *)curr_metadata->next) {
      curr_metadata->size += curr_metadata->next->size + sizeof(my_metadata_t);
      curr_metadata->next = curr_metadata->next->next;
    }
    // 次のメタデータに移動
    prev_metadata = curr_metadata;
    curr_metadata = curr_metadata->next;
  }
}


void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // テストケース1: メモリの割り当てと解放
  void *ptr1 = my_malloc(16);
  assert(ptr1 != NULL);
  my_free(ptr1);

  // テストケース2: メモリの割り当て、解放、再度の割り当て
  void *ptr2 = my_malloc(32);
  assert(ptr2 != NULL);
  my_free(ptr2);
  void *ptr3 = my_malloc(16);
  assert(ptr3 != NULL);
  my_free(ptr3);

  // テストケース3: 複数のオブジェクトの割り当てと異なる順序での解放
  void *ptr4 = my_malloc(64);
  assert(ptr4 != NULL);
  void *ptr5 = my_malloc(128);
  assert(ptr5 != NULL);
  void *ptr6 = my_malloc(32);
  assert(ptr6 != NULL);
  my_free(ptr5);
  my_free(ptr6);
  my_free(ptr4);
}

