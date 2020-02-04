# https://unix.stackexchange.com/a/40646/185953
setopt prompt_subst

# Get git ideas from https://github.com/ohmyzsh/ohmyzsh/wiki/External-themes
# play with colors at https://zsh-prompt-generator.site/
# TODO: git functions in https://github.com/ohmyzsh/ohmyzsh/blob/master/lib/git.zsh
# fast git? https://github.com/ohmyzsh/ohmyzsh/blob/a85ce89a3dc7fc63b4e8518a923f9c718561eb0b/themes/refined.zsh-theme#L42
# consider doing something special if connected via SSH: https://github.com/KorvinSilver/blokkzh/blob/master/blokkzh.zsh-theme#L49
# easiest git integration: https://scriptingosx.com/2019/07/moving-to-zsh-06-customizing-the-zsh-prompt/
# TODO: experiment with vcs stuff
# http://zsh.sourceforge.net/Doc/Release/User-Contributions.html#Version-Control-Information
# prompt %vars: http://zsh.sourceforge.net/Doc/Release/Prompt-Expansion.html#Prompt-Expansion
# url auto-complete, tetris: https://matt.blissett.me.uk/linux/zsh/zshrc
# https://unix.stackexchange.com/a/214699/185953
# zstyle ':completion:*' menu select  # THIS DOES THE COMPLETION FROM MENU STUFF :D

color() {
    local -r color_code="$1"
    local -r text="$2"
    echo "%F{$color_code}$text%f"
}

# Virtualenv: current working virtualenv
virtualenv_prompt_info() {
    # https://github.com/ohmyzsh/ohmyzsh/blob/96f4a938383e558e8f800ccc052a80c6f743555d/plugins/virtualenv/virtualenv.plugin.zsh
    # -n means length of string is non-zero
    # "${VIRTUAL_ENV:t}" == "$(basename $VIRTUAL_ENV)"
    if [[ -n $VIRTUAL_ENV ]]; then
        echo "${VIRTUAL_ENV:t}"
    fi
}


# NOTE that doing this will probably stomp over oh-my-zsh
precmd() {
    virtualenv_prompt_info_var="$(virtualenv_prompt_info)"
}

# Put these calculations in an anonymous function so locals don't leak to
# environment when this script is sourced
function {
    local -r red=196
    # if $? == 0 then nothing else 'red '
    local -r return_code="%(?..$(color $red '%?') )"

    local -r orange=214
    local -r timestamp="$(color $orange '%D{%H:%M:%S.%. %Z}')"

    local -r purple=147
    local -r short_hostname="$(color $purple '%m')"

    local -r light_blue=45
    local -r current_directory="$(color $light_blue '%~')"

    local -r yellow=226
    # if UID == 0 then '#' else '$'
    local -r prompt_character="$(color $yellow '%(!.#.$)')"

    # an uninterpolated stirng (single quotes on purpose)
    # this var will undergo prompt_subst and be overwritten by precmd
    local -r green=47
    local -r virtualenv_prompt_info_var="$(color $green '$virtualenv_prompt_info_var')"

    # NOTE: return code includes it's own spacing (so it doesn't go here)
    export VIRTUAL_ENV_DISABLE_PROMPT=1
    export PROMPT="$return_code$timestamp $short_hostname:$current_directory $virtualenv_prompt_info_var
$prompt_character "
}

unfunction color

