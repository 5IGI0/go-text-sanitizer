package gotextsanitizer

import "bytes"

// Convert UTF-8 string into an ASCII representation of it.
//
// Please note that perfect transliteration is not guaranteed.
// It is not intended to be used for primary display purposes, but rather for secondary purposes.
// such as urls, tags, etc.
//
// If you have any corrections/comments to make about the transliteration, please report it at https://github.com/avian2/unidecode.
// This function is only a port of this library and the mapping is generated directly from it.
// if it's not about transliteration (error, crash, ...) you should report it to me.
func Unidecode(input string) (string, error) {
	var ret bytes.Buffer

	for _, r := range input {
		if r < 127 {
			ret.WriteRune(r)
			continue
		}

		block := uint16(r >> 8)

		if (uint(r) >> 8) > 0xFFFF {
			continue
		}

		if tbl, e := defaultUnidecodeMap[block]; e {
			if len(tbl) > int(r&0xFF) {
				ret.WriteString(tbl[int(r&0xFF)])
			}
		}
	}

	return ret.String(), nil
}
