#set -x

num_lines=$(( 3 * 10 ** 6 ))

text='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

rm in/sample.csv

echo 'mensagens' >> in/sample.csv

echo 'Gerando arquivo de exemplo: sample.csv'

for counter in $(seq 1 $num_lines);
do
    echo "$text" >> in/sample.csv
done

echo 'FEITO!'