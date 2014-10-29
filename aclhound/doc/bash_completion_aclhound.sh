# START aclhound completion
# This file is in the public domain
# See: http://www.debian-administration.org/articles/317 for how to write more.
# Usage: Put "source bash_completion_aclhound.sh" into your .bashrc
_aclhound() 
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    opts=" \
    init \
    fetch \
    task \
    diff \
    build \
    reset"
    
    case "${prev}" in
        task)
            local opts="\
                status \
                list \
                submit \
                start \
                clean"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        diff)
            local opts="all $(ls)"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        build)
            local opts="all $(ls)"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        *)
            ;;
    esac

    COMPREPLY=($(compgen -W "${opts}" -- ${cur}))  
    return 0

}
complete -F _aclhound aclhound

# END aclhound completion


 	  	 
