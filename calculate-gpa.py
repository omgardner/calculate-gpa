import pandas as pd


def opener(filepath, mode='r'):
    with open(filepath, mode=mode) as file:
        return file.read()


def sum_from_keys(d,key_list):
    # return sum of values that have a key in the key_list
    total = 0
    for key,val in d.items():
        if key in key_list:
            total += val
            
    return total


def calculate_gpa(grade_counts,scale=4,verbose=True):
    if scale is 4:
        w = sum_from_keys(grade_counts,['HD','D'])
        x = sum_from_keys(grade_counts,['CR'])
        y = sum_from_keys(grade_counts,['P'])
        e = sum(grade_counts.values()) - sum_from_keys(grade_counts,['W', 'S'])
        f = sum_from_keys(grade_counts,['F'])
        
        gpa = (4*w + 3*x + 2*y + 0*f) / e
        if verbose: print('HD+D:{0}\tCR:{1}\tP:{2}\tTotal:{3}\tFailed:{4}'.format(w,x,y,e,f))
        return gpa

    elif scale is 7:
        v = sum_from_keys(grade_counts,['HD'])
        w = sum_from_keys(grade_counts,['D'])
        x = sum_from_keys(grade_counts,['CR'])
        y = sum_from_keys(grade_counts,['P'])
        e = sum(grade_counts.values()) - sum_from_keys(grade_counts,['W', 'S'])
        f = sum_from_keys(grade_counts,['F'])
        gpa = (7*v+ 6*w + 5*x + 4*y + 0*f) / e
        
        if verbose: print('HD:{0}\tD:{1}\tCR:{2}\tP:{3}\tTotal:{4}\tFailed:{5}'.format(v,w,x,y,e,f))
        return gpa
    else:
        if verbose: print('Invalid scale value')
        return None


def main(filepath=None, scale=None, verbose=False):
	# split paste data into a list of lists
	t_raw = opener(filepath).strip()
	transcript = [line.split('\t') for line in t_raw.split('\n')]
	t_df = pd.DataFrame(transcript[1:], columns=transcript[0])

	# multiply unit counts by 3 to get credit counts for each grade
	grade_counts = dict(t_df.Grade.value_counts()*3)
	gpa = calculate_gpa(grade_counts, scale, verbose)

	print(gpa)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Calculate GPA based on transcript copied from estudent.")
	parser.add_argument('scale', help="4 or 7 point scale",type=int, default=4)
	parser.add_argument('-f', '--filepath', help="filepath to the pasted transcript", default='pasted-results.txt')
	parser.add_argument('-v','--verbose', help="Print more.", action='store_true', default=False)
	args = parser.parse_args()
	main(**vars(args))