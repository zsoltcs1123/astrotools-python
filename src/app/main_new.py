from datetime import datetime
from core.position import Position
from core.position_factory import PositionFactory
from objects.points import NN, SN


if __name__ == "__main__":
    dt = datetime.now()
    factory = PositionFactory()
    nn = factory.create_position(NN, dt)
    sn = factory.create_position(SN, dt)
    
    print(nn)
    print('\n----\n')
    print(sn)