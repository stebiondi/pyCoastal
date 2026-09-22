-- Inline code that can break across lines, for the LaTeX build.
--
-- Identifiers such as applications.structures or tolerable_use="trained_staff"
-- are long and have no spaces, so in a table cell or a justified line they
-- run into the margin. This sets inline code as \texttt with a permitted
-- break after the characters a reader expects a code line to wrap at, and
-- never a hyphen (the typewriter face has hyphenation switched off).

local BREAK_AFTER = {
  ["."] = true, ["_"] = true, ["("] = true, [","] = true,
  ["/"] = true, ["="] = true, ["["] = true,
}

local ESCAPE = {
  ["\\"] = "\\textbackslash{}", ["#"] = "\\#", ["$"] = "\\$",
  ["%"] = "\\%", ["&"] = "\\&", ["_"] = "\\_", ["{"] = "\\{",
  ["}"] = "\\}", ["~"] = "\\textasciitilde{}", ["^"] = "\\textasciicircum{}",
}

function Code(el)
  if not FORMAT:match("latex") then
    return nil
  end
  local out = {}
  for _, cp in utf8.codes(el.text) do
    local c = utf8.char(cp)
    out[#out + 1] = ESCAPE[c] or c
    if BREAK_AFTER[c] then
      out[#out + 1] = "\\allowbreak{}"
    end
  end
  return pandoc.RawInline("latex", "\\texttt{" .. table.concat(out) .. "}")
end
