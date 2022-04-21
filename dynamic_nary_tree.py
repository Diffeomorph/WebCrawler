
class Node:
    """
    Sets up a node class for a particular url. It contains a children array which holds
    pointers to each of the child nodes/links of this url. This children array has variable
    size.
    """
    def __init__(self, url):
        self.url = url
        self.children = []
        
class DynamicNaryTree:
    """
    This class uses the Node class to create an N-ary tree with varying N sizes for each node.
    """
    def __init__(self):
        self.root = None
        self.d = {}
        
    def create_tree(self, parent_child_array):  
        """
        Given a list of (child, parent) relationships, build the corresponding tree of links.
        """

        # put all child nodes from the parent_child_array in nodes and store in dictionary
        for i, value in enumerate(parent_child_array):
            self.d[value[0]] = Node(value[0])
     
        # represents the root node of tree
        root_ = None
     
        # traverse the parent_child_array list and build the tree
        for i, value in enumerate(parent_child_array):
     
            # if the parent is -1, this node is the root of the tree
            if value[1] == -1:
                root_ = self.d[value[0]]
            else:
                # get the parent for the current node
                ptr =self. d[value[1]]
                ptr.children.append(self.d[value[0]])
        
        self.root = root_        
        return
    
    def print_ntree(self, node, flag,depth,is_last):
        """
        Parameters
        ----------
        node : given node to print from
        flag : is a dictionary from depth ---> boolean representing whether to keep searching at this depth
        depth : current depth of the tree
        is_last : is this node the end of the tree

        Returns
        -------
        Graphical representation of the tree.

        """
    
        if node == None:
            return
           
        # Loop to print the depths of the
        # current node
        for i in range(1, depth):
            # Condition when the depth is exploring
            if flag[i]:
                print("| ","", "", "", end = "")
               
            # Otherwise print the blank spaces
            else:
                print(" ", "", "", "", end = "")
           
        if depth == 0:
            print(node.url)
        elif is_last:
            print("+---", node.url)
            # No more childrens turn it
            # to the non-exploring depth
            flag[depth] = False
        else:
            print("+---", node.url)
       
        it = 0
        for i in node.children:
            it+=1
            # Recursive call for the
            # children nodes
            self.print_ntree(i, flag, depth + 1, it == (len(node.children) - 1))
        flag[depth] = True
     
        