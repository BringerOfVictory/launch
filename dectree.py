import pandas as pd

classes = ['M', 'B']

# Split a dataset based on an attribute and an attribute value
def test_split(index, value, dataset):
   left, right = pd.DataFrame(), pd.DataFrame()
   for i, row in dataset.iterrows():
      if row[index] < value:
         left = left.append(row.to_frame().transpose())
      else:
         right = right.append(row.to_frame().transpose())
   return [left, right]

# Calculate the Gini index for a split dataset
def gini_index(groups, class_values):
   gini = 0.0
   for class_value in class_values:
      for group in groups:
         size = len(group.index)
         if size == 0:
            continue
         proportion = (group['diagnosis'] == class_value).sum() / float(size)
         gini += (proportion * (1.0 - proportion))
   return gini

# Select the best split point for a dataset
def get_split(dataset):
   class_values = ['M', 'B']
   b_index, b_value, b_score, b_groups = 999, 999, 999, None
   for attribute in list((dataset.columns.values))[2:12]:
      for index, row in dataset.iterrows():
         groups = test_split(attribute, row[attribute], dataset)
         gini = gini_index(groups, class_values)
         #print('X[%s] < %.3f Gini=%.3f' % ((attribute), row[attribute], gini))
         if gini < b_score:
            b_index, b_value, b_score, b_groups = attribute, row[attribute], gini, groups
   print('index=', b_index, 'value=', b_value, 'gini=', b_score)
   return {'index':b_index, 'value':b_value, 'groups':b_groups}

# Create a terminal node value
def to_terminal(group):
   outcomes = [row[-1] for row in group]
   return max(set(outcomes), key=outcomes.count)

# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):
   left, right = node['groups']
   del(node['groups'])
   # check for a no split
   if not left or not right:
      node['left'] = node['right'] = to_terminal(left + right)
      return
   # check for max depth
   if depth >= max_depth:
      node['left'], node['right'] = to_terminal(left), to_terminal(right)
      return
   # process left child
   if len(left) <= min_size:
      node['left'] = to_terminal(left)
   else:
      node['left'] = get_split(left)
      split(node['left'], max_depth, min_size, depth+1)
   # process right child
   if len(right) <= min_size:
      node['right'] = to_terminal(right)
   else:
      node['right'] = get_split(right)
      split(node['right'], max_depth, min_size, depth+1)

# Build a decision tree
def build_tree(train, max_depth, min_size):
   root = get_split(train)
   split(root, max_depth, min_size, 1)
   return root

# Print a decision tree
def print_tree(node, depth=0):
   if isinstance(node, dict):
      print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
      print_tree(node['left'], depth+1)
      print_tree(node['right'], depth+1)
   else:
      print('%s[%s]' % ((depth*' ', node)))

dataset = pd.read_csv("data.csv")
sample = dataset.head()
#print(sample)
#print()
get_split(dataset)
