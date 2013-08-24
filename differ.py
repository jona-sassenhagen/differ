# This is where a hashbang will go if I someday decide they aren't voodoo.

# GUTHRIE LICENSE
# This work is protected by US laws and anybody caught using it 
# without our permission will be mighty good friends of ourn 
# cause we don’t give a dern. Publish it. Edit it. Run it. 
# Sell it. Yodel it. We wrote it, that’s all we wanted to do.

import os, sys

# This program takes two strings and attempts find the changes between the 
# initial and final string by returning a new string marked up in the 
# "Critic Markup" style.

# Critic Markup is a sort of text-based tracked changes, probably inspired by 
# Markdown, the human-readable markup for blogs and comments.
# See: http://criticmarkup.com/spec.php

# Note: this is apparently just how diff works, from the early 70s. 
#   maybe check out Diff-Text for more ideas on detecting moved 
#  blocks of text. 

#  Also, some way to interact specifically with 
#    Word's tracked changes would be ideal. Oh, wait, someone 
#    has done that too, it's just already in Word
#    Create a Track Changes Document by Comparing Two Microsoft Word Files
#      - John Garger
#    http://bit.ly/WcXpx3

# TODO:
#   1. Better tokens, don't bother looking for substrings character by 
#      character, but word by word. This would improve both efficiency and 
#      readability. Two birds, one stone. Yeah, using tokens from the start
#      would've been smart.
#      Note: currently, readability is hacked by ignoring any common substrings
#      that lack a space. That's something, but nothing for efficiency.
#   2. More efficient LCS algorithm - Ukkonen's Suffix Trees? So hard...
#   3. command line arguments to operate on files, parseargs?


def longest_common_substring(S1, S2):
  # find common substring len 1 or return None

  # there are better algorithms, maybe suffix trees? 
  
  best_substring = ""
  for best_length in range(len(S1)):
    for index in range(len(S1)):
      if index + best_length + 1 > len(S1):
        break
      if S1[index:index + best_length + 1] in S2:
        best_substring = S1[index:index+best_length+1]
        break
  return best_substring

def many_pass_markup(old_string, new_string):
  # hopper = [full old string, full new string]
  # final = ''
  # checkout and compare first two items in hopper
  # 1. if identical, write once to final
  # 2. if completely different, no common substring, write to end of final 
  #      with markup. eg, final = '{--old--}{++new++}'
  # 3. if some common substring, push back into front of hopper as so:
  #      [...] -> [old.pre, new.pre, lcs, lcs, old.post, new.post, ...]
  #   Note: duplicating the longest common substring allows us to check out
  #         two items every time without thinking
  # 4. return to checkout step until hopper empty
  hopper = [old_string, new_string]
  final_string = ""
  while len(hopper) > 0:
    old_string, new_string, hopper = hopper[0], hopper[1], hopper[2:]
    if old_string == new_string:
      final_string += old_string
    else:
      lcs = longest_common_substring(old_string, new_string)
      if lcs == None or " " not in lcs:
      # the '" " not in lcs' chunk improves readability of markup
      # it makes sure changes aren't detected letter by letter
      # this should be removed once tokens are fixed
        lcs = ""
      if lcs == "":
        if old_string != "":
          final_string = final_string + "{--" + old_string + "--}"
        if new_string != "":
          final_string = final_string + "{++" + new_string + "++}"
      else:
          lcs_length = len(lcs)
          # find index 
          old_lcs_index = old_string.find(lcs)  
          new_lcs_index = new_string.find(lcs)
          old_pre = old_string[:old_lcs_index]
          new_pre = new_string[:new_lcs_index]
          old_post = old_string[old_lcs_index + lcs_length:]
          new_post = new_string[new_lcs_index + lcs_length:]
          old_hopper = hopper
          hopper = [old_pre, new_pre, lcs, lcs, old_post, new_post]
          hopper.extend(old_hopper)
  return final_string
      
def main():
  if sys.hexversion < 0x03000000:
    print("""
This program is designed for Python 3,
older versions may lead to instability. 

(In fact, they'll probably flat out break.)
           
Python 3 includes enhancements to improve
speed and reduce ambiguity in the language,
I highly recommend it. It can be downloaded
here: 

http://www.python.org/getit/""")
    exit()

  num_args = len(sys.argv)

## DE-COMMENT WHEN FINISHED TESTING ##
  if num_args != 4:
    print("Usage: differ.py original_file revised_file results_file")
    return False
  
  
  original_filename = sys.argv[1]
  revised_filename = sys.argv[2]
  results_filename = sys.argv[3]
## END COMMENT
## TEST VALUES ##
  
  # original_filename = "king james.txt"
  # revised_filename = "douay-rheims.txt"
  # results_filename = "tmp.txt"
  
## END TEST VALUES ##
  
  directory = os.getcwd()
  
  original_fullpath = os.path.join(directory,original_filename)
  revised_fullpath = os.path.join(directory,revised_filename)
  results_fullpath = os.path.join(directory,results_filename)

  with open(original_fullpath,mode='r',encoding='utf-8') as original_object:
    with open(revised_fullpath,mode='r',encoding='utf-8') as revised_object:
      with open(results_fullpath,mode='w',encoding='utf-8') as results_object:

        original_text = ""
        for line in original_object:
          original_text += line
        
        revised_text = ""
        for line in revised_object:
          revised_text += line
      
        results_text = many_pass_markup(original_text, revised_text)
      
        results_object.write(results_text)
      
        print(original_text)
        print()
        print(revised_text)
        print()
        print()
        print(results_text)
  
if __name__ == "__main__":
  # i have mixed feelings about this construct, not everything needs to dual 
  # hat as a library and a standalone...
  main()
