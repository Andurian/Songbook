\layout {
  \context {
    \ChordNames
    \override ChordName.font-shape = #'italic
    \override ChordName.font-size = #3
  }
  \context{
    \Lyrics
    \override LyricText.font-size = #2
  }
}

boxedSectionLabel = 
  #(define-music-function
      (s1)
      (string?)
    #{ \sectionLabel \markup { \large \bold { \box #s1 } } #})

boxedSectionLabelWithComment = 
  #(define-music-function
      (s1 s2)
      (string? string?)
    #{ \sectionLabel \markup { \large \bold { \box #s1 } (#s2) } #})
