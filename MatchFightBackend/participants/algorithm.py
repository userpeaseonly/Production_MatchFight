def sort_participants(participants):
    return sorted(participants, key=lambda p: p.weight)

def generate_pairs(participants, level):
    sorted_participants = sort_participants(participants)
    pairs = []

    if len(sorted_participants) <= 4:
        return []  # Do not create pairs if less than 4 participants

    if len(sorted_participants) % 2 != 0:
        if level % 2 == 0:
            for participant in sorted_participants:
                if not participant.miss:
                    sorted_participants.remove(participant)
                    participant.miss = True
                    pairs.append((participant, None))
                    break
        else:
            middle_index = len(sorted_participants) // 2
            participant = sorted_participants[middle_index]
            if participant.miss:
                participant = sorted_participants[middle_index + 1]
            sorted_participants.remove(participant)
            participant.miss = True
            pairs.append((participant, None))

    for i in range(0, len(sorted_participants), 2):
        pairs.append((sorted_participants[i], sorted_participants[i + 1]))

    return pairs
