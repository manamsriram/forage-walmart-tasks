public class MaxHeap {

    private Integer branchingFactor;
    public java.util.List<Integer> elements = new java.util.ArrayList<>();

    public MaxHeap(Integer exponent) {
        if (exponent < 0 || exponent > 30) {
            throw new IllegalArgumentException("Exponent must be between 0 and 30 inclusive");
        }
        this.branchingFactor = 1 << exponent;

    }

    public Integer popMax() {
        if (elements.isEmpty()) {
            return null;
        }
        Integer maxElement = elements.get(0);
        elements.set(0, elements.get(elements.size() - 1));
        elements.remove(elements.size() - 1);
        // Re-heapify the heap after removing the max element
        this.siftDown(0);
        return maxElement;            
    }

    public void insert(Integer element) {
        elements.add(element);
        int currentIndex = elements.size() - 1;
        this.siftUp(currentIndex);
    }

    private void siftDown(int currentIndex) {
        while (true) {
            int largestIndex = currentIndex;
            // check if firstChildIndex and lastChildIndex are within bounds of an Integer for safety
            // for large branching factors, the multiplication could overflow an Integer, so we use Long type for safety
            Long firstChildIndex = (long) currentIndex * branchingFactor + 1;
            Long lastChildIndex = Math.min((long) currentIndex * branchingFactor + branchingFactor, (long) elements.size() - 1);
            for (long i = firstChildIndex; i <= lastChildIndex; i++) {
                if (elements.get((int)i) > elements.get(largestIndex)) {
                    largestIndex = (int)i;
                }
            }
            if (largestIndex == currentIndex) {
                break;
            }
            Integer temp = elements.get(currentIndex);
            elements.set(currentIndex, elements.get(largestIndex));
            elements.set(largestIndex, temp);
            currentIndex = largestIndex;
        }
    }

    private void siftUp(int currentIndex) {
        while (currentIndex > 0) {
            int parentIndex = (currentIndex - 1) / branchingFactor;
            if (elements.get(currentIndex) > elements.get(parentIndex)) {
                Integer temp = elements.get(currentIndex);
                elements.set(currentIndex, elements.get(parentIndex));
                elements.set(parentIndex, temp);
                currentIndex = parentIndex;
            } else {
                break;
            }
        }
    }
}