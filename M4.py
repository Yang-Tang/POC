"""
M4
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    bla
    """
    matrix = dict()
    for row in (alphabet | set(['-'])):
        matrix[row] = dict()
        for col in (alphabet | set(['-'])):
            if (row == '-' or col == '-'):
                score = dash_score
            elif row == col:
                score = diag_score
            else:
                score = off_diag_score
            matrix[row][col] = score
    return matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    bla
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    matrix = [[0 for dummy_col in range(len_y + 1)] for dummy_row in range(len_x + 1)]
    for row in range(1, len_x + 1):
        score = matrix[row - 1][0] + scoring_matrix[seq_x[row - 1]]['-']
        if (not global_flag) and score < 0:
            score = 0
        matrix[row][0] = score
    for col in range(1, len_y + 1):
        score = matrix[0][col - 1] + scoring_matrix['-'][seq_y[col - 1]]
        if (not global_flag) and score < 0:
            score = 0
        matrix[0][col] = score
    for row in range(1, len_x + 1):
        for col in range(1, len_y + 1):
            score1 = matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]
            score2 = matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-']
            score3 = matrix[row][col - 1] + scoring_matrix['-'][seq_y[col - 1]]
            score = max(score1, score2, score3)
            if (not global_flag) and score < 0:
                score = 0
            matrix[row][col] = score
    return matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    bla
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    align_x = ''
    align_y = ''
    score = alignment_matrix[len_x][len_y]
    while len_x <> 0 and len_y <> 0:
        if alignment_matrix[len_x][len_y] == alignment_matrix[len_x-1][len_y-1] + scoring_matrix[seq_x[len_x-1]][seq_y[len_y-1]]:
            align_x = seq_x[len_x-1] + align_x
            align_y = seq_y[len_y-1] + align_y
            len_x -= 1
            len_y -= 1
        elif alignment_matrix[len_x][len_y] == alignment_matrix[len_x-1][len_y] + scoring_matrix[seq_x[len_x-1]]['-']:
            align_x = seq_x[len_x-1] + align_x
            align_y = '-' + align_y
            len_x -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[len_y-1] + align_y
            len_y -= 1
    while len_x <> 0:
        align_x = seq_x[len_x-1] + align_x
        align_y = '-' + align_y
        len_x -= 1
    while len_y <> 0:
        align_x = '-' + align_x
        align_y = seq_y[len_y-1] + align_y
        len_y -= 1
    return (score, align_x, align_y)
        
def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    bla
    """
    lenx = len(seq_x)
    leny = len(seq_y)
    align_x = ''
    align_y = ''
    score = -1
    for idx_x in range(lenx + 1):
        for idx_y in range(leny + 1):
            new_score = alignment_matrix[idx_x][idx_y]
            if new_score > score:
                score = new_score
                len_x = idx_x
                len_y = idx_y
    while alignment_matrix[len_x][len_y] > 0:
        if alignment_matrix[len_x][len_y] == alignment_matrix[len_x-1][len_y-1] + scoring_matrix[seq_x[len_x-1]][seq_y[len_y-1]]:
            align_x = seq_x[len_x-1] + align_x
            align_y = seq_y[len_y-1] + align_y
            len_x -= 1
            len_y -= 1
        elif alignment_matrix[len_x][len_y] == alignment_matrix[len_x-1][len_y] + scoring_matrix[seq_x[len_x-1]]['-']:
            align_x = seq_x[len_x-1] + align_x
            align_y = '-' + align_y
            len_x -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[len_y-1] + align_y
            len_y -= 1
    return (score, align_x, align_y)
        
    

print build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
# s = build_scoring_matrix('ATGC', 10, 4, -1)
# seq_x = 'AAAGCCC'
# seq_y = 'AAACCC'
# m = compute_alignment_matrix(seq_x, seq_y, s, False)
# print m
# print compute_local_alignment(seq_x, seq_y, s, m)