import timeit
import argparse
from rag.pipeline import build_rag_pipeline
import json
import time
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_rag_response(query, chain, debug=False):
    result = chain.query(query)

    try:
        # Convert and pretty print
        data = json.loads(str(result))
        data = json.dumps(data, indent=4)
        return data
    except (json.decoder.JSONDecodeError, TypeError):
        print("The response is not in JSON format.")

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs',
                        type=str,
                        default='invoice_number',
                        help='Enter the query to pass into the LLM')
    parser.add_argument('types',
                        type=str,
                        default='int',
                        help='Enter types of elements passed in the query')
    parser.add_argument('--debug',
                        action='store_true',
                        default=False,
                        help='Enable debug mode')
    args = parser.parse_args()

    start = timeit.default_timer()

    query = 'retrieve ' + args.inputs
    query_types = args.types

    query_inputs_arr = [param.strip() for param in args.inputs.split(',')]
    query_types_arr = [param.strip() for param in query_types.split(',')]

    rag_chain = build_rag_pipeline(query_inputs_arr, query_types_arr, args.debug)

    step = 0
    answer = False
    while not answer:
        step += 1
        if step > 1:
            print('Refining answer...')
            # add wait time, before refining to avoid spamming the server
            time.sleep(5)
        if step > 3:
            # if we have refined 3 times, and still no answer, break
            answer = 'No answer found.'
            break
        print('Retrieving answer...')
        answer = get_rag_response(query, rag_chain, args.debug)

    end = timeit.default_timer()

    print(f'\nJSON answer:\n{answer}')
    print('=' * 50)

    print(f"Time to retrieve answer: {end - start}")