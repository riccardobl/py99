P="python3"
X="$P py99.py"

rm -Rf build/tmp
mkdir -p build/tmp

function runTest {
    $X tests/$1.py99 build/tmp/$1.py
    out=`$P build/tmp/$1.py`
    expected=`cat tests/results/$1.txt`
    if [ "$out" == "$expected" ]; then
        echo "$1: OK!"
    else
        echo "$1: Failed."
        exit 1
    fi
}

runTest test1
runTest test2
runTest test3
runTest test4
runTest test5
runTest test6