#!/bin/sh
# kesekit UserPromptSubmit hook: when a prompt asks for a security check ("보안점검",
# "보안 점검"), add context telling Claude to start with the kesekit skills.
# Reads the hook JSON on stdin. POSIX sh + grep + sed only (no Python/Node needed).
# Never blocks or fails a prompt: every path exits 0.

payload=$(cat) || exit 0

# Keep only the text from the "prompt" value on (the payload is single-line JSON and the
# prompt comes after cwd/transcript_path, so folder names cannot trigger the hook).
prompt=$(printf '%s' "$payload" | sed -n 's/.*"prompt"[[:space:]]*:[[:space:]]*"//p')
[ -n "$prompt" ] || exit 0

# An explicit slash command already picks its own skill.
case "$prompt" in
  /*) exit 0 ;;
esac

printf '%s' "$prompt" | grep -Eq '보안[[:space:]]*점검' || exit 0

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"\uc0ac\uc6a9\uc790 \uba54\uc2dc\uc9c0\uc5d0 \"\ubcf4\uc548\uc810\uac80\"\uc774 \uc788\uc2b5\ub2c8\ub2e4. \uc0c8\ub85c \ubcf4\uc548 \uc810\uac80\uc744 \uc694\uccad\ud55c \uac83\uc774\uba74 \ub2e4\ub978 \uc791\uc5c5\ubcf4\ub2e4 \uba3c\uc800 Skill \ub3c4\uad6c\ub85c `kesekit:kesekit-start-ko` \uc2a4\ud0ac\uc744 \uc2e4\ud589\ud558\uc138\uc694. \uc694\uccad\uc774 \ub354 \uad6c\uccb4\uc801\uc774\uba74 \ub9de\ub294 kesekit \uc2a4\ud0ac\uc744 \ub300\uc2e0 \uc501\ub2c8\ub2e4: \ubc30\ud3ec \uc804 \uccb4\ud06c\ub9ac\uc2a4\ud2b8\ub294 `kesekit:kesekit-check-ko`, \ucde8\uc57d\uc810 \uc218\uc815\u00b7\ud558\ub4dc\ub2dd\uc740 `kesekit:kesekit-fix-ko`, KISA \ubcf4\uc548\uacf5\uc9c0\u00b7\ud328\uce58\u00b7CVE \ud655\uc778\uc740 `kesekit:kesekit-advisory-ko`. \uc774\ubbf8 \uc9c4\ud589 \uc911\uc774\uac70\ub098 \ub05d\ub09c \uc810\uac80\uc5d0 \ub300\ud55c \uc9c8\ubb38\uc774\uba74 \uc774 \uc548\ub0b4\ub294 \ubb34\uc2dc\ud569\ub2c8\ub2e4. kesekit \uc2a4\ud0ac\uc744 \uc4f8 \uc218 \uc5c6\uc73c\uba74 \uadf8 \uc0ac\uc2e4\uc744 \uc54c\ub9ac\uace0 \uc77c\ubc18 \uc810\uac80\uc73c\ub85c \uc9c4\ud589\ud569\ub2c8\ub2e4."}}'
exit 0
