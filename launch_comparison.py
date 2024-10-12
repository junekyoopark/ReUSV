import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

# Data for Vehicle A
n_A = 391  # Total launches
k_A = int(n_A * 0.9923)  # Successful launches
p_hat_A = k_A / n_A  # Observed success rate

# Data for Vehicle B
n_B = 2  # Total launches
k_B = 2  # Successful launches
p_hat_B = k_B / n_B  # Observed success rate

print(f"Vehicle A: {k_A} successes out of {n_A} launches ({p_hat_A*100:.2f}% success rate)")
print(f"Vehicle B: {k_B} successes out of {n_B} launches ({p_hat_B*100:.2f}% success rate)")

# 1. Confidence Intervals using the Clopper-Pearson method (Exact Binomial Confidence Interval)
confidence_level = 0.95
alpha = 1 - confidence_level

# Confidence Interval for Vehicle A
ci_A = stats.binom.interval(confidence_level, n_A, p_hat_A, loc=0)
lower_ci_A = ci_A[0] / n_A
upper_ci_A = ci_A[1] / n_A

# Confidence Interval for Vehicle B
ci_B = stats.binom.interval(confidence_level, n_B, p_hat_B, loc=0)
lower_ci_B = ci_B[0] / n_B
upper_ci_B = ci_B[1] / n_B

print("\n95% Confidence Intervals (Clopper-Pearson Method):")
print(f"Vehicle A: ({lower_ci_A*100:.2f}%, {upper_ci_A*100:.2f}%)")
print(f"Vehicle B: ({lower_ci_B*100:.2f}%, {upper_ci_B*100:.2f}%)")

# 2. Hypothesis Testing for Proportions
# Null Hypothesis H0: p_A >= p_B
# Alternative Hypothesis H1: p_A < p_B

# Since n_B is small, we use Fisher's Exact Test
from statsmodels.stats.proportion import proportions_ztest, proportion_confint, proportions_chisquare

count = np.array([k_A, k_B])
nobs = np.array([n_A, n_B])

# Using normal approximation (Not suitable for small n, but included for completeness)
stat, p_value = proportions_ztest(count, nobs, alternative='smaller')
print("\nHypothesis Testing (Proportions Z-test):")
print(f"Z-test statistic: {stat:.4f}")
print(f"P-value: {p_value:.4f}")

# 3. Bayesian Inference
# Using Beta distribution as the conjugate prior for the binomial likelihood
from scipy.stats import beta

# Prior parameters (Assuming non-informative prior)
alpha_prior = 1
beta_prior = 1

# Posterior for Vehicle A
posterior_A = beta(alpha_prior + k_A, beta_prior + n_A - k_A)
mean_A = posterior_A.mean()
cred_interval_A = posterior_A.interval(confidence_level)

# Posterior for Vehicle B
posterior_B = beta(alpha_prior + k_B, beta_prior + n_B - k_B)
mean_B = posterior_B.mean()
cred_interval_B = posterior_B.interval(confidence_level)

print("\nBayesian Inference Results:")
print(f"Vehicle A Posterior Mean: {mean_A*100:.2f}%")
print(f"Vehicle A 95% Credible Interval: ({cred_interval_A[0]*100:.2f}%, {cred_interval_A[1]*100:.2f}%)")
print(f"Vehicle B Posterior Mean: {mean_B*100:.2f}%")
print(f"Vehicle B 95% Credible Interval: ({cred_interval_B[0]*100:.2f}%, {cred_interval_B[1]*100:.2f}%)")

# Plotting the posterior distributions
x = np.linspace(0, 1, 1000)
plt.figure(figsize=(10,6))
plt.plot(x, posterior_A.pdf(x), label='Vehicle A Posterior', lw=2)
plt.plot(x, posterior_B.pdf(x), label='Vehicle B Posterior', lw=2)
plt.title('Posterior Distributions of Success Rates')
plt.xlabel('Success Rate')
plt.ylabel('Density')
plt.legend()
plt.grid(True)
plt.show()
