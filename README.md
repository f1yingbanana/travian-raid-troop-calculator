# :crossed_swords: travian-raid-troop-calculator

Travian Raid Troop Calculator is a Python tool used to calculate how many troops you should build given the farms around you. It is designed to calculate an optimal number of troops to build to rush for a second village within the beginner's protection period.

Note that this tool uses your cookie to scan the map around your village. However, this tool does not automate any actions on the account or resemble any premium features, and thus should be exempt from §3 of [game rules](https://www.travian.com/us/gamerules). However, I still strongly recommend you to review the code to ensure that the cookie is not being used in a malicious way and make your own decision whether to utilize this tool or not.

## :hammer_and_wrench: Prerequisites

* Python 3
* Python packages (available on [pip](https://pypi.org/project/pip/))
  * `cv2`
  * `numpy`
  * `requests`

## :page_with_curl: How to use

1. Clone or download this repo.
2. Run the following and follow the prompt:
```
python <containing-folder-path>/calculator.py
```
3. When prompted about JWT, log into Travian and retrieve your JWT from your browser cookies.
   * On Chrome, this value is `Menu > More tools > Developer tools > Application > Storage > Cookies > JWT`

This should give you something like the following:

![Sample tool output](docs/sample-output.png)

You can also edit the `calculator.py` and pre-populate some fields to save some time over repeated runs. Here are a list of parameters that you can tune:

* `server`: the server you are playing on, e.g. `'ts1.x1.america.travian.com'`
* `jwt`: find in your browser cookie, see above
* `unit`: one of the following:
  * `dm.Troop.CLUBSWINGER`
  * `dm.Troop.LEGIONNAIRE`
  * `dm.Troop.EQUITES_IMPERATORIS`
  * `dm.Troop.PHALANX`
  * `dm.Troop.THEUTATES_THUNDER`
  * You may also define your own or add more in `datamodels.py`
* `target_roi`: return of investment in hours, e.g. 48
* `efficiency`: how efficient you are at farming, from 0-1
* `location`: location of your village

## :mortar_board: Theory

In an ideal scenario, we are the only farmer and all farms never overflow. A farm is characterized by its production rate $P_f$ and distance $D_f$ from the farmer. A troop is characterized by its speed $S_t$, production cost $C_t$, carrying capacity $W_t$, and upkeep $K_t$.

It follows that to be able to empty the resources of a farm $f$, we need the following amount of troops per hour:

$$R_f = \frac{P_f}{W_t}$$

A troop is occupied when it is out farming. It spends $2D_f/S_t$ hours on the way. Therefore we need the following amount of troops to exhaust a farm non-stop:

$$N_f = \frac{2R_fD_f}{S_t} = \frac{2P_fD_f}{S_tW_t}$$

This costs $N_fC_t$ to build, and $N_fK_t$ for the crop cost per hour, which we can reduce from $P_f$. Thus the return of investment (ROI) is:

$$T_{\text{ROI}} = \frac{N_fC_t}{P_f-N_fK_t} = \frac{\frac{2P_fD_f}{S_tW_t}C_t}{P_f-\frac{2P_fD_f}{S_tW_t}K_t} = \frac{2D_fC_t}{S_tW_t - 2D_fK_t}$$

Note that $T_{\text{ROI}}$ only depends on the farm's distance, and does not depend on its production.

Given a target ROI $T_{\text{Target}}$, we can thus find the maximum distance for a particular type of troop:

$$D_{\text{ROI}} = \frac{T_{\text{Target}}S_tW_t}{2C_t+2T_{\text{Target}}K_t}$$

To find the number of troops to build, we can sum $N_f$ for each farm within $D_{\text{ROI}}$ of the farmer:

$$N = \sum_{f | D_f < D_{\text{ROI}}} N_f$$

The calculation above assumes perfect farm. To account for farming competition from other players, we introduce an efficiency factor $e, 0 < e \le 1$, which represents how much farm we are getting from the sources:

$$T_{\text{ROI}} = \frac{N_fC_t}{eP_f - N_fK_t} = \frac{2D_fC_t}{eS_tW_t - 2D_fK_t}$$

Similarly, $D_{\text{ROI}}$ is now:

$$D_{\text{ROI}} = \frac{eT_{\text{Target}}S_tW_t}{2C_t+2T_{\text{Target}}K_t}$$

As expected, this increases $T_{\text{ROI}}$, which reduces $D_{\text{ROI}}$ and $N$.

The calculation above still assumes that all troops are built instantly and all oases are clear of wild animals. We can again account for this by tuning $e$ when running the script.
