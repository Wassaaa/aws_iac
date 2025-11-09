#include "InverseCumulativeNormal.h"
#include <cstdlib>
#include <iomanip>
#include <iostream>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <probability_percent>\n";
        std::cerr << "Example: " << argv[0] << " 95.0\n";
        return 1;
    }

    // Parse input as percentage (0-100)
    double percent = std::atof(argv[1]);

    // Validate input range
    if (percent <= 0.0 || percent >= 100.0) {
        std::cerr << "Error: Probability must be between 0 and 100 (exclusive)\n";
        return 1;
    }

    // Convert percentage to probability (0-1)
    double probability = percent / 100.0;

    // Calculate inverse cumulative normal (z-score)
    quant::InverseCumulativeNormal icn; // mean=0, sigma=1
    double z_score = icn(probability);

    // Output result with high precision
    std::cout << std::fixed << std::setprecision(16) << z_score << std::endl;

    return 0;
}
