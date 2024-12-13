from argument_parser import make_parser


def read_file(file_name: str) -> str:
    with open(file_name, 'r', encoding='utf8') as fh:
        line = fh.readline()
    return line.strip()


def map_to_blocks(input_map: str) -> list[int]:
    blocks = []
    # writing files at first
    file_mode = 1
    file_id = 0
    for char in input_map:
        length = int(char)
        if file_mode:
            for i in range(length):
                blocks.append(file_id)
            file_id += 1
        else:
            for i in range(length):
                blocks.append(-1)
        # switch mode
        file_mode = abs(file_mode - 1)
    return blocks


def move_blocks(input_blocks: list[int]) -> list[int]:
    first_empty = input_blocks.index(-1)
    moving = len(input_blocks) - 1
    while moving > first_empty:
        if input_blocks[moving] != -1:
            moved_id = input_blocks[moving]
            input_blocks[first_empty] = moved_id
            input_blocks[moving] = -1
        moving -= 1
        first_empty = input_blocks.index(-1)
    return input_blocks


def string_to_ids_with_counts(input_blocks: list[int]) -> tuple[list[int], list[int]]:
    # transform list of all blocks into blocks + sizes
    new_blocks, new_counts = [], []
    prev_id = input_blocks[0]
    id_count = 0
    for i, block in enumerate(input_blocks):
        current_id = block
        if current_id == prev_id:
            id_count += 1
            continue
        else:
            new_blocks.append(prev_id)
            new_counts.append(id_count)
            id_count = 1
        prev_id = current_id
    new_blocks.append(prev_id)
    new_counts.append(id_count)
    return new_blocks, new_counts


def ids_with_count_to_string(blocks_and_counts: tuple[list[int], list[int]]) -> str:
    output = ""
    blocks, counts = blocks_and_counts
    for b, c in zip(blocks, counts):
        for i in range(c):
            output += str(b)
    return output


def move_files(blocks_and_counts: tuple[list[int], list[int]]) -> tuple[list[int], list[int]]:
    blocks, counts = blocks_and_counts

    # find the largest file id
    for el in blocks[::-1]:
        if el != -1:
            max_file_id = el
            break

    for file_id in reversed(range(max_file_id + 1)):
        first_empty = blocks.index(-1)
        first_empty_size = counts[first_empty]
        moving = blocks.index(file_id)
        moving_size = counts[moving]

        while moving > first_empty:
            if first_empty_size == moving_size:
                blocks = blocks[:first_empty] + [file_id] + blocks[first_empty+1:moving] + [-1] + blocks[moving+1:]
                counts = counts[:first_empty] + [moving_size] + counts[first_empty+1:moving] + [first_empty_size] + counts[moving+1:]
                break
            elif first_empty_size > moving_size:
                difference = first_empty_size - moving_size
                blocks = blocks[:first_empty] + [file_id] + blocks[first_empty:moving] + [-1] + blocks[moving+1:]
                counts = counts[:first_empty] + [moving_size] + [difference] + counts[first_empty+1:moving] + [moving_size] + counts[moving+1:]
                break
            elif first_empty_size < moving_size:
                first_empty += blocks[first_empty+1:].index(-1) + 1
                first_empty_size = counts[first_empty]

    return blocks, counts


def checksum(blocks: list[int]) -> int:
    total = 0
    for i, block in enumerate(blocks):
        if block != -1:
            total += i * block
    return total


def checksum_from_blocks_and_counts(blocks_and_counts: tuple[list[int], list[int]]) -> int:
    total = 0
    i = 0
    for block, count in zip(blocks_and_counts[0], blocks_and_counts[1]):
        for c in range(count):
            if block != -1:
                total += i * block
            i += 1
    return total


if __name__ == '__main__':
    args = make_parser().parse_args()
    in_blocks = map_to_blocks(read_file(args.input))
    # print("".join([str(ch) for ch in blocks]))
    if args.part == 1:
        # print("".join([str(ch) for ch in move_blocks(map_to_blocks(read_file(args.input)))]))
        print(checksum(move_blocks(in_blocks)))
    elif args.part == 2:
        # print("".join([str(el) for el in in_blocks]))
        print(checksum_from_blocks_and_counts(move_files(string_to_ids_with_counts(in_blocks))))
        # print(ids_with_count_to_string(move_files(string_to_ids_with_counts(in_blocks))))
