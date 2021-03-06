package sudoku

import (
	"fmt"
	"strconv"
)

// Board :
type Board [][]int

// NewBoard :
func NewBoard(n int) Board {
	out := make([][]int, n*n)
	for i := range out {
		out[i] = make([]int, n*n)
	}
	return out
}

// Copy :
func (board Board) Copy() Board {
	out := make([][]int, len(board))
	for r, row := range board {
		out[r] = make([]int, len(row))
		copy(out[r], row)
	}
	return out
}

func printBoard(board Board) {
	out := ""
	for _, row := range board {
		for _, val := range row {
			out += strconv.Itoa(val) + " "
		}
		out += "\n"
	}
	fmt.Println(out)
}
